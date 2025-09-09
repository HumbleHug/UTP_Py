import random as rd
lista = []
for i in range(10):
    lista.append(rd.randint(1, 100)) #genera numeros del 1 al 100
print("Lista de numeros:", lista) #muestra la lista
n = len(lista) #len muestra la longitud (cantidad de elementos de la lista)
for i in range(n-1): #recorre la lista varias veces
    for j in range(0, n-i-1): #compara los elementos adyacentes
        if lista[j] > lista[j + 1]:
            lista[j], lista[j + 1] = lista[j + 1], lista[j] #ordena la lista simple de arriba
print("Ascendente:", lista) #Orden ascendente
print("Descendente:", lista[::-1])  #lista[::-1] copia la lista y lo imprime al reves