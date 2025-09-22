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

# Generación de datos
ejex=[i for i in range (30)]    # Eje X: lista de valores de 0 a 29
ejey=np.sin(aleatorio(30))      # Serie 1: seno de valores aleatorios
ejey2=np.cos(aleatorio(30))     # Serie 2: coseno de valores aleatorios
ejey3=np.array(ejey)-np.array(ejey2)    # Serie 3: diferencia entre ejey y ejey2

# Configuración de figura y subplots
fig,axs = plt.subplots(2,2)     # Figura con cuadrícula 2x2 (4 espacios para gráficas)
figtitle="grafico comparativo de valores aleatorios"    # Título general de la figura
fig.suptitle(figtitle.upper(),fontdict={'fontweight': 'bold'})    

# Subplot (0,0): sen(aleatorio)
axs[0,0].plot(ejex,ejey,'go--')     # Gráfico verde con círculos y línea discontinua
axs[0,0].set_title("datos aleatorios 1")      

# Subplot (0,1): cos(aleatorio)
axs[0,1].plot(ejex,ejey2,"rx:")     # Gráfico rojo con cruces y línea punteada
axs[1,1].set_xlabel("cantidad")

# Subplot (1,0): diferencia sen - cos
axs[1, 0].plot(ejex, ejey3, 'b-.')  # Gráfico azul con línea punteada-dash
axs[1, 0].set_title("sen - cos")

# Subplot (1,1): vacío con cuadrícula
axs[1, 1].set_xlabel("cantidad")  # Etiqueta del eje X
axs[1,1].grid()     # Activa cuadrícula (queda como espacio libre)

plt.tight_layout()   # Ajusta para que no se sobrepongan los textos
plt.show()