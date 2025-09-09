import datetime as dt
import random as rd
nombre = "Ing. Oscar Lopez"
fecha = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
valores = []
for i in range(15):
    v = rd.randint(0, 1023) 
    if v < 100:
        valores.append(f"Valor bajo: {v}")
    elif v < 500:
        valores.append(f"Valor medio: {v}")
    else:
        valores.append(f"Valor alto: {v}")

print("=========================================")
print("           CORREO DE REPORTE")
print("=========================================")
print(f"De: {nombre}")
print(f"Fecha: {fecha}\n")
print("Estimado ingeniero en jefe,")
print("Adjunto los valores de tensión medidos en la fecha indicada:\n")

for valor in valores:
    print(valor)

print("\nSaludos cordiales,")
print("Sistema de Monitoreo Automático")
print("=========================================")