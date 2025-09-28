import matplotlib.pyplot  as plt
import numpy as np

def aleatorio(n=20):
        #Docstring
    """permite generar numeros aleatorios de valor entero entre 1 y 30 y da de salida una lista de valores

    Args:
        n (int, optional): numero el datos ingresados. Defecto 20.
    """
    import random as rd
    Value=[] #lista vacia
    for i in range (n): #incio de un bucle es con el : el identado es importante
        Value.append(rd.randint(1,30)) #append añade a la lista\
    return(Value) #lo que devuelve la funcion

ejex=[i for i in range (30)]
ejey=np.sin(aleatorio(30))
ejey2=np.cos(aleatorio(30))
ejey3=np.array(ejey)-np.array(ejey2)
figtitle="grafico comparativo de valores aleatorios"
plt.title(figtitle.upper(),fontdict={'fontweight': 'bold'})     #TITULO
plt.xlabel("numero de datos")   #TITULO en el eje x
plt.ylabel("valores aleatorios")    #TITULO en el eje y
plt.plot(ejex,ejey,color="#10144bd3",marker='x', linestyle='--',linewidth=3, markersize=6,label="aleatorio 1") #(ejex, ejey, caracteristicas)
plt.plot(ejex,ejey2,'b--^',linewidth=1, markersize=5,label="aleatorio 2") #(ejex, ejey, caracteristicas)
plt.plot(ejex,ejey3,'g',linewidth=2, markersize=5,label="aleatorio 2") #(ejex, ejey, caracteristicas)
plt.legend()    #genera leyenda
plt.grid()      #genera 
plt.show()      #grafica la imagen