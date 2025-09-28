import numpy as np                 # Librería para cálculos numéricos y manejo de arrays
import matplotlib.pyplot as plt    # Librería para graficar

# ------------------------------------#
# cálculo del sistema de armónicos
# x(t)=A*sin(2*pi*f*t+theta_0)

dt = [i for i in range(200)]       # Lista de 0 a 199 (índices de tiempo)
t = np.array(dt) * 0.03            # Vector de tiempo con paso de 0.03 s

# Variables de los armónicos
A = [3, 3]                          # Amplitudes
f = [1, 0.67]                        # Frecuencias (Hz)
theta_i = [0.26, 1.45]               # Fases iniciales (radianes)

# Cálculo de las señales
x1 = A[0] * np.sin(2 * np.pi * f[0] * t + f[0])       # Primer armónico
x2 = A[1] * np.sin(2 * np.pi * f[1] * t + theta_i[1]) # Segundo armónico
xaco = np.array(x1) + np.array(x2)                    # Suma (acoplamiento) de ambos

# Parte gráfica
fig, axs = plt.subplots(3)           # Figura con 3 subgráficos
figtitle = "Funciones armonicas y sus acoplados"
fig.suptitle(figtitle.upper(), fontdict={'fontweight': 'bold'})  # Título principal en negrita

# Gráfico 1: primer armónico
axs[0].plot(t, x1, color="#10144bd3", marker='x', linestyle='--', linewidth=2, markersize=3)  # Curva x1
axs[0].set_title(f"Armonico con valores (A,f,thetao)={A[0], f[0], theta_i[0]}")  # Título
axs[0].set_xticks([])                # Sin marcas en eje X
axs[0].grid()                        # Activa rejilla
axs[0].set_ylim(-7, 7)                # Límites Y

# Gráfico 2: segundo armónico
axs[1].plot(t, x2, color="#52d46cd2", marker='o', linestyle='-', linewidth=2, markersize=3)  # Curva x2
axs[1].set_title(f"Armonico con valores (A,f,thetao)={A[1], f[1], theta_i[1]}")  # Título
axs[1].set_xticks([])                # Sin marcas en eje X
axs[1].grid()                        # Activa rejilla
axs[1].set_ylim(-7, 7)                # Límites Y

# Gráfico 3: señal acoplada
axs[2].plot(t, xaco, color="#ff8400d2", marker='^', linestyle=':', linewidth=2, markersize=3)  # Curva suma
axs[2].grid()                        # Activa rejilla
axs[2].set_ylim(-7, 7)                # Límites Y

# Guardar la figura en PDF
plt.savefig('AcoplamientoArmonico.pdf', bbox_inches="tight", pad_inches=0.5, dpi=1080,
            edgecolor="b", facecolor="#ffffffff")  # Exporta gráfico a PDF
