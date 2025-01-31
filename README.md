# Challenge Robotique

## Méthode utilisé

Nous avons décidé d'utiliser un algorithme colonie de fourmis pour essayer de résoudre le problème par une méthode de renforcement.

Les essais d'optimisation sur les récompenses et sur l'utilisation du fuel, nous avons décider d'optimiser au maximum la distance à parcourir sur le parcours total.

Le programme antColony est notre première version de l'algorithme, malheuresement l'optimisation sur la distance à parcourir n'est pas terrible et varie bien trop lorsque l'on relance le programme de multiple fois. 
C'est pour cela que nous avons antColony_v2, la version finale du programme, qui permet une certaine convergence de la distance à parcourir.

Nous sommes censé commencer la simulation avec 10000 de fuel mais actuellement nous en avons 20000. 
Pour y remédier nous avons rajouté une condition qui essaie de calculer le fuel dépensé et qui renvoit directement FINISH une fois que l'on a moins de 10000 de fuel.
Si jamais on voudrait retirer cette partie du code il suffit de retirer la condition :

```py
if self.fuel > 0
```
du code antColony et la condition :

```py
if aco.fuel > 0
```
du code antColony_v2

## Lancement

Avant de lancer la simulation, il suivi tout d'abord de modifier le nom de la map à utiliser en 'donnees-map.txt' puis de lancer le programme python antColony_v2. Il suffit ensuite de lancer la simulation.
