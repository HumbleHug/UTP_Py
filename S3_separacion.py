import random as rd

v_in = [] #lista vacia 
for i in range(15): #inicia el bucle con el i
    v_in.append(rd.randint(1, 10)) #da valores entre el 1-10

V_may = []
V_men = []
for i in v_in:
    if i >= 5: #lo clasifica si es menor a 5
        V_may.append(i)
    else:
        V_men.append(i)
print(V_may)
print(V_men)
