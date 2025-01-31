# Challenge Robotique

## Méthode utilisée

Nous avons décidé d'utiliser un algorithme de colonie de fourmis pour résoudre le problème par une méthode de renforcement.

Les essais d'optimisation sur les récompenses et sur l'utilisation du fuel n'ont pas été concluants. Nous avons donc décidé d'optimiser au maximum la distance à parcourir sur l'ensemble du parcours.

Le programme antColony est notre première version de l'algorithme. Malheureusement, l'optimisation de la distance à parcourir n'est pas satisfaisante et varie trop lorsque l'on relance le programme plusieurs fois.
C'est pourquoi nous avons développé antColony_v2, la version finale du programme, qui permet une meilleure convergence de la distance à parcourir.

Nous sommes censés commencer la simulation avec 10 000 unités de fuel, mais nous en avons actuellement 20 000.
Pour y remédier, nous avons ajouté une condition qui calcule le fuel dépensé et renvoie directement FINISH dès que nous avons moins de 10 000 unités de fuel.
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

Avant de lancer la simulation, il suffit tout d'abord de modifier le nom de la map à utiliser en 'donnees-map.txt' puis de lancer le programme python antColony_v2. Il suffit ensuite de lancer la simulation.
