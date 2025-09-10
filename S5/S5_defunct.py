import random as rd

def conversor(V):
    """una funcion que recibe voltaje y retorna los valores de temperatura

    Args:
        V (float) / no tiene que ser una lista: voltaje de ingreso y que se cambiara a temperatura
    """
    Temp=12*V-15
    return Temp

def aleatorio(n=20):
    """genera numeros aleatorios, si no se indica el numero se generan automaticamente 20 valores

    Args:
        n (int, optional): numero de valores aleatorios - si no se indica genera 20
    """
    Vingreso=[] #lista vacia
    for i in range (n): #incio de un bucle es con el : el identado es importante
        Vingreso.append(rd.randint(1,30)) #append añade a la lista\
    return(Vingreso)

def clasificar_alerta(temp_c, umbral=100.0):
    """Devuelve 'ALERTA' si temp_c > umbral, si no 'OK'."""
    return "ALERTA" if temp_c > umbral else "OK"
    
def main():
    """Solo se ejecuta cuando corres este archivo directamente."""
    valores = aleatorio(30)
    temperaturas = [conversor(v) for v in valores]
    alertas = [clasificar_alerta(t, 150) for t in temperaturas]
    print("Voltajes:", valores)
    print("Temperaturas:", [round(t, 2) for t in temperaturas])
    print("Alertas:", alertas)



#para usar las paqueterias internas (def) del programa en otro programa
if __name__ == "__main__":
    main()  # solo se ejecuta al correr: python s4_pipeline.py