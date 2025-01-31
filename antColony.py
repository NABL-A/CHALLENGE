import numpy as np
import math
import random

b = 3
b0 = 100
α = 0.0698
V0 = 1 
T = 600

class GraphAndRobot():
    def __init__(self, nodes, edges):
        self.nodes = nodes  # Clé : coordonnées, Valeur : (points, masse, index)
        self.edges = edges  # Matrice des distances
        self.poidsRobot = 0
        self.recompense = 0
        self.positionRobot = [0, 0, 0]  # x, y, theta
        self.fuel = 10000  # Carburant initial
        self.alpha = 0.1  # Influence des phéromones
        self.beta = 2.0  # Influence de l'inverse de la distance
        self.evaporation_rate = 0.5  # Taux d'évaporation des phéromones
        self.pheromones = []  # Matrice des phéromones

        donnees = []
        coordonnees = []
        map = open("donnees-map.txt", "r")
        lines = map.readlines()
        for line in lines:
            donnees.append(line.split("   "))
        map.close()

        self.taille = len(donnees)
        self.edges = [[0 for _ in range(self.taille)] for _ in range(self.taille)]

        for i in range(self.taille):
            coordonnees.append((float(donnees[i][0]), float(donnees[i][1])))
            if '1' in donnees[i][2]:
                self.nodes[(float(donnees[i][0]), float(donnees[i][1]))] = (1, 1, i)
            elif '2' in donnees[i][2]:
                self.nodes[(float(donnees[i][0]), float(donnees[i][1]))] = (2, 2, i)
            else:
                self.nodes[(float(donnees[i][0]), float(donnees[i][1]))] = (3, 2, i)

        for i in range(self.taille):
            for j in range(self.taille):
                self.edges[i][j] = round(self.distance(coordonnees[i], coordonnees[j]), 2)

        self.pheromones = [[1 for _ in range(self.taille)] for _ in range(self.taille)]

    def distance(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    
    def v_max(self):
        return V0*math.exp(-α * self.poidsRobot)
    
    def conso_fuel(self,distance):
        return (b*self.poidsRobot + b0)*distance

    def choose_next_point(self, current_index, visited):
        probabilities = []
        for i in range(self.taille):
            if i not in visited:
                pheromone = self.pheromones[current_index][i] ** self.alpha
                heuristic = (1 / self.edges[current_index][i]) ** self.beta
                probabilities.append(pheromone * heuristic)
            else:
                probabilities.append(0)

        total = sum(probabilities)
        if total == 0:
            return None  

        probabilities = [p / total for p in probabilities]

        return random.choices(range(self.taille), weights=probabilities, k=1)[0]

    def update_pheromones(self, paths, scores):
        for i in range(self.taille):
            for j in range(self.taille):
                self.pheromones[i][j] *= (1 - self.evaporation_rate)

        for path, score in zip(paths, scores):
            for i in range(len(path) - 1):
                self.pheromones[path[i]][path[i + 1]] += 1 / score

    def run_ant_colony(self, iterations, num_ants):
        best_path = None
        best_score = float('inf')

        for _ in range(iterations):
            paths = []
            scores = []

            for _ in range(num_ants):
                current_index = 0 
                visited = {current_index}
                path = [current_index]
                total_distance = 0

                while len(visited) < self.taille:
                    next_index = self.choose_next_point(current_index, visited)
                    if next_index is None:
                        break

                    total_distance += self.edges[current_index][next_index]
                    visited.add(next_index)
                    path.append(next_index)
                    current_index = next_index

                paths.append(path)
                scores.append(total_distance)

                if total_distance < best_score:
                    best_score = total_distance
                    best_path = path

            self.update_pheromones(paths, scores)

        return best_path, best_score

    def write_actions(self, best_path):
        actions = []
        script = open("script.txt", "w")

        liste = list(self.nodes.keys())

        start_position = (0, 0) 
        self.positionRobot = [0, 0, 0]  

        for i in range(len(best_path)):
            if i == 0:  
                current_position = start_position
                self.recompense += self.nodes[liste[best_path[i]]][0]

            else:
                current_position = list(self.nodes.keys())[best_path[i - 1]]
                self.recompense += self.nodes[liste[best_path[i]]][0]



            next_index = best_path[i]
            next_position = list(self.nodes.keys())[next_index]

            
            desired_angle = math.atan2(next_position[1] - current_position[1], next_position[0] - current_position[0])

            angle_to_turn = desired_angle - self.positionRobot[2]
            angle_to_turn = (angle_to_turn + math.pi) % (2 * math.pi) - math.pi
            angle_to_turn = angle_to_turn * (180 / math.pi)

            dist = self.distance(current_position, next_position)

            self.positionRobot[0] = next_position[0]
            self.positionRobot[1] = next_position[1]
            self.positionRobot[2] = desired_angle

            if self.fuel > 0 :
                actions.append(f"TURN {angle_to_turn}\n")
                actions.append(f"GO {dist}\n")
            
            self.poidsRobot += self.nodes[liste[best_path[i]]][1]
            self.fuel -= self.conso_fuel(dist)

        actions.append("FINISH\n")
        script.writelines(actions)
        script.close()

if __name__ == '__main__':
    graphe_carte = GraphAndRobot({}, [])
    best_path, best_score = graphe_carte.run_ant_colony(iterations=100, num_ants=50)
    print("Meilleur chemin trouvé :", best_path)
    print("Score (distance totale) :", best_score)
    graphe_carte.write_actions(best_path)
    print(graphe_carte.poidsRobot)
    print(graphe_carte.recompense)

