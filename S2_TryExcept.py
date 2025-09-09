valor_txt = input("ingrese los valores de Temperatura en C: ")
try: #para posibles errores en datos de ingreso
    t=float(valor_txt)
    if t >= 10: #condicion if "condicion 1": para el ambito matematico
        print("Alerta! Alta Temperatura")
    elif t < 0: #condicion 2
        print("temperatura bajo 0")
    else:
        print("Temperatura normal")
except ValueError:
    print("Entrada inválida. Use números (ej. 26.5).")