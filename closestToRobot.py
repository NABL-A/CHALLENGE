import numpy as np
import math

b = 10**(-2)
b0 = 10**(-2)
fuel = 10**4
α = 0.0698
V0 = 1 


def main():

    graphe_carte = GraphAndRobot({},[])
    graphe_carte.deplacementPlusProche()

def distance(a ,b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def ecrireActions():
    script = open("script.txt","w")

    listeActions = []
    for i in range(10):
        listeActions.append("TURN 90\n")
        listeActions.append(f"GO {i}\n")
    listeActions.append("FINISH")

    script.writelines(listeActions)






class GraphAndRobot():
    def __init__(self, nodes, edges):
        self.nodes = nodes # Dictionnaire : clé -> 2-uplet (coordonnées) et valeur -> 3-uplet (value, masse, numéro cylindre)
        self.edges = edges # Matrice : Mi,j correspond à la distance entre les cylindres i et j

        self.poidsRobot = 0
        self.positionRobot = [0,0,0] # x,y,θ(en degré)
        self.recompense = 0

        donnees = []
        coordonnees = []
        map = open("donnees-map.txt", "r")
        lines = map.readlines()
        for line in lines:
            donnees.append(line.split("   "))
        map.close()

        self.taille = len(donnees)
        self.edges = [[0 for i in range(self.taille)] for j in range(self.taille)]

        for i in range(self.taille):

            coordonnees.append((float(donnees[i][0]),float(donnees[i][1])))

            if '1' in donnees[i][2]:
                self.nodes[(float(donnees[i][0]),float(donnees[i][1]))] = (1,1,i)
            elif '2' in donnees[i][2]:
                self.nodes[(float(donnees[i][0]),float(donnees[i][1]))] = (2,2,i)
            else :
                self.nodes[(float(donnees[i][0]),float(donnees[i][1]))] = (3,2,i)

        
        for i in range(self.taille):
            for j in range(self.taille):
                self.edges[i][j] = round(distance(coordonnees[i],coordonnees[j]),2)

          
    def v_max(self):
        return V0*math.exp(-α * self.poidsRobot)


    def deplacementPlusProche(self):
        actions = []
        script = open("script.txt","w")
        liste = list(self.nodes.keys())

        for iterations in range(len(liste)):
            #print(liste)
            min = 1000
            for i,cle in enumerate(liste):
                if distance(self.positionRobot[:2],cle) < min and distance(self.positionRobot[:2],cle) > 0:
                    min = distance(self.positionRobot[:2],cle)
                    index = self.nodes[liste[i]][2]
                    erase = i
            print(f"Vitesse max : {self.v_max()}")
            self.recompense += self.nodes[liste[erase]][0]
            print(f"Recompense : {self.recompense}")
            self.poidsRobot += self.nodes[liste[erase]][1]
            print(f"Poids robot : {self.poidsRobot}")

            print(f"Min : {min} et index : {index}\n")

            desired_angle = math.atan2((liste[erase][1]-self.positionRobot[1]),(liste[erase][0]-self.positionRobot[0]))

            angle_to_turn = desired_angle - self.positionRobot[2]
            angle_to_turn = (angle_to_turn + math.pi)%(2*math.pi) - math.pi
            angle_to_turn = angle_to_turn*(180/math.pi)

            dist = distance(self.positionRobot[:2],liste[erase])

            self.positionRobot[0] = liste[erase][0]
            self.positionRobot[1] = liste[erase][1]
            self.positionRobot[2] = desired_angle


            liste.pop(erase)
            actions.append(f"TURN {angle_to_turn}\n")
            actions.append(f"GO {dist}\n")
        
        actions.append("FINISH")

        script.writelines(actions)




if __name__ == '__main__' :
    main()

