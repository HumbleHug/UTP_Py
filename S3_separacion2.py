#import random as rd
#Vingreso=[] #lista vacia
#for i in range (20): #incio de un bucle es con el : el identado es importante
#    Vingreso.append(rd.randint(1,30)) #append añade a la lista
#print(Vingreso) 

Vingreso=[20,40,10,15,3,6,12,4] #valores ingresados por archivo, comando o lecturas
Vmayor=[]
Vmenor=[]
for i in Vingreso:
    if i >= 15:
        Vmayor.append(i)
    else:
        Vmenor.append(i)
print(Vmayor)
print(Vmenor)

Vmayor.sort()
print(Vmayor)


suma=0
for i in range(1,10):
    suma=suma+1/(i*(i+1))
print(suma)