import numpy as np
import math
import random

b = 3
b0 = 100
α = 0.0698
V0 = 1 
T = 600

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def angle(a,b,robotAngle):
    desired_angle = math.atan2(b[1] - a[1], b[0] - a[0])
    angle_to_turn = desired_angle - robotAngle
    angle_to_turn = (angle_to_turn + math.pi) % (2 * math.pi) - math.pi
    angle_to_turn = angle_to_turn * (180 / math.pi)
    return desired_angle, angle_to_turn

class GraphAndRobot:
    def __init__(self, nodes, edges, alpha=1.0, beta=2.0, evaporation_rate=0.3, ants=200, iterations=10000):
        self.nodes = nodes
        self.edges = edges
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.ants = ants
        self.iterations = iterations
        self.taille = len(nodes)
        self.pheromones = np.ones((self.taille, self.taille))
        self.best_path = None
        self.best_score = float('inf')
        self.convergence_threshold = 10  
        self.position = [0,0]
        self.poidsRobot = 0
        self.angle = 0
        self.fuel = 10000
    
    def choose_next_point(self, current_index, visited):
        probabilities = []
        for i in range(self.taille):
            if i not in visited:
                pheromone = self.pheromones[current_index][i] ** self.alpha
                heuristic = (1 / self.edges[current_index][i]) ** self.beta if self.edges[current_index][i] > 0 else 0
                probabilities.append(pheromone * heuristic)
            else:
                probabilities.append(0)
        
        total = sum(probabilities)
        if total == 0:
            return None  
        
        probabilities = [p / total for p in probabilities]
        return random.choices(range(self.taille), weights=probabilities, k=1)[0]
    
    def update_pheromones(self, paths, scores):
        self.pheromones *= (1 - self.evaporation_rate)
        for path, score in zip(paths, scores):
            pheromone_deposit = 1 / score  
            for i in range(len(path) - 1):
                self.pheromones[path[i]][path[i + 1]] += pheromone_deposit
    
    def conso_fuel(self, dist):
        return (b*self.poidsRobot + b0)*dist

    def run(self):
        best_found = 0
        
        for iteration in range(self.iterations):
            paths = []
            scores = []

            for _ in range(self.ants):
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

                if total_distance < self.best_score:
                    self.best_score = total_distance
                    self.best_path = path
                    best_found = iteration
            
            self.update_pheromones(paths, scores)
            
            if iteration - best_found > self.convergence_threshold:
                print(f"Convergence atteinte à l'itération {iteration}")
                break
        
        return self.best_path, self.best_score


donnees = []
coordonnees = []

maptxt = open("donnees-map.txt", "r")
lines = maptxt.readlines()
for line in lines:
    donnees.append(line.split("   "))

for i in range(len(donnees)):
    if '1' in donnees[i][2]:
        donnees[i][2] = 1
    else:
        donnees[i][2] = 2
    donnees[i] = list(map(float,donnees[i]))
maptxt.close()

for i in range(len(donnees)):
    coordonnees.append((float(donnees[i][0]),float(donnees[i][1])))

edges = np.zeros((len(coordonnees), len(coordonnees)))
for i in range(len(coordonnees)):
    for j in range(len(coordonnees)):
        edges[i][j] = distance(coordonnees[i], coordonnees[j])

aco = GraphAndRobot(coordonnees, edges)
best_path, best_score = aco.run()

script = open("script.txt", "w")

for i in range(len(best_path)):
    if aco.fuel > 0 :
        angleTurn = angle(aco.position,coordonnees[best_path[i]],aco.angle)[1]
        script.write(f"TURN {angleTurn}\n")
        aco.angle = angle(aco.position,coordonnees[best_path[i]],aco.angle)[0]

        distanceGo = distance(aco.position,coordonnees[best_path[i]])
        script.write(f"GO {distanceGo}\n")
        aco.position[0] = coordonnees[best_path[i]][0]
        aco.position[1] = coordonnees[best_path[i]][1]

        aco.poidsRobot += donnees[i][2]
        aco.fuel -= aco.conso_fuel(distanceGo)

script.write("FINISH")

print(donnees)
print(f"Meilleur chemin trouvé : {best_path}")
print(f"Distance totale : {best_score}")
