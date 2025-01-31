liste = [1,2,3,4]

donnees = [['2.4','4.5',1],['2.4','4.5']]

for i in liste[:-1]:
    print(i)

for i in range(len(donnees)):
    donnees[i] = list(map(float,donnees[i]))

print(donnees)