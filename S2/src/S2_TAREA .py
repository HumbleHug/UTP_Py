UMBRAL_BAJO = 3.50     
UMBRAL_MEDIO = 4.50    
UMBRAL_ALTO = 5.00     

alumno = input("Ingrese el nombre del alumno o equipo: ") #input = pide escribir
equipo = input("Ingrese el código del equipo: ")

try:
    num_muestras = int(input("Ingrese el número de muestras registradas: "))
except ValueError:
    print("Error: el número de muestras debe ser un número entero.")
    exit()

try:
    lectura1 = float(input("Ingrese la primera lectura (en voltios): "))
    lectura2 = float(input("Ingrese la segunda lectura (en voltios): "))
except ValueError:
    print("asdasError: las lecturas deben ser valores numéricos (float).")
    exit()

promedio = (lectura1 + lectura2) / 2

if promedio < UMBRAL_BAJO:
    estado = "BAJO"
elif promedio < UMBRAL_MEDIO:
    estado = "MEDIO"
elif promedio < UMBRAL_ALTO:
    estado = "NORMAL"
else:
    estado = "ALTO"

print("\n=== REPORTE DE SENSOR ===")
print(f"Alumno/Equipo : {alumno} | Equipo: {equipo}")
print(f"N° de muestras: {num_muestras}")
print(f"Lecturas (V)  : {lectura1:.2f}, {lectura2:.2f} | Promedio: {promedio:.2f} V")
print(f"Estado        : {estado}")