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
ejey2 = -ejey

# Configuración de figura y subplots
fig, axs = plt.subplots(1,2)     # Figura con cuadrícula 1x2 (2 espacios para gráficas)
figtitle="Funciones sen(x) y -sen(x)"    # Título general de la figura
fig.suptitle(figtitle.upper(),fontdict={'fontweight': 'bold'})    

# Subplot (0): sen(x)
axs[0].plot(ejex,ejey,'g',label="sen(x)")     # Gráfico verde línea continua
axs[0].set_title("sen(x)")                    # Título del subplot
axs[0].legend()                               # Muestra la leyenda

# Subplot (1): -sen(x)
axs[1].plot(ejex,ejey2,'r--',label="-sen(x)") # Gráfico rojo línea discontinua
axs[1].set_title("-sen(x)")                   # Título del subplot
axs[1].legend()                               # Muestra la leyenda

plt.tight_layout()   # Ajusta para que no se sobrepongan los textos

# Guarda la figura actual en un archivo de imagen
plt.savefig(
    'salida_sen.png',     # Nombre del archivo de salida (formato depende de la extensión: .jpg, .png, .pdf, etc.)
    bbox_inches="tight", # Ajusta el cuadro de la figura al contenido, eliminando espacios en blanco innecesarios
    pad_inches=0.8,      # Margen extra alrededor de la figura (en pulgadas)
    dpi=1080,            # Resolución de la imagen: puntos por pulgada (alta calidad con 1080)
    edgecolor="b",       # Color del borde externo de la figura ("b" = azul)
    facecolor="#dcc8d9d4" # Color de fondo de la figura (en formato hexadecimal RGBA)
)