def pedir_peticion():
    """
    En la petición, si empieza con '.', el resto será la 'respuesta secreta'.
    Si no empieza con '.', se devuelve el texto normal.
    """
    peticion = input("Petición: ")

    if peticion.startswith("."):
        # Guardamos la respuesta oculta
        respuesta_secreta = peticion[1:].strip()
        # Mostramos algo "normal", como hacía la web
        print("Pedro, por favor responde a mi pregunta")
        return respuesta_secreta
    else:
        # No hay truco, no se esconde nada
        print(peticion)
        return None


def pedir_pregunta(respuesta_secreta):
    pregunta = input("Pregunta: ")
    if respuesta_secreta:
        print("Pedro responde:", respuesta_secreta)
    else:
        print("Pedro responde: No tengo respuesta...")


# Programa principal
while True:
    print("\n--- JUEGO PEDRO RESPONDE ---")
    secreta = pedir_peticion()
    pedir_pregunta(secreta)

    salir = input("\n¿Quieres salir? (s/n): ")
    if salir.lower() == "s":
        break
