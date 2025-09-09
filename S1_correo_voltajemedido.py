import datetime as dt
import random as rd
nombre = "Ing. Oscar Lopez"
fecha = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
edad = 29
v = rd.randint(0, 1023)

activo = True
print(f"Estimado ingeniero en jefe, {nombre}. Edad:{edad}")
print(f"Fecha: {fecha}\n")
print(f"voltaje medido: {v:5f}, V/Activo:{activo}")