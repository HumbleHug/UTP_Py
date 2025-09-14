# peter_answers.py

def mostrar_peticion(secreto):
    # Frase que se muestra en pantalla aunque por dentro se guarda la respuesta
    frase_visible = "Peter, please answer the following question..."
    # Trucazo: aunque parece que escribes la frase visible,
    # en realidad guardas la respuesta secreta
    return frase_visible, secreto


def peter_answers():
    print("=== Bienvenido a Peter Answers (versión educativa) ===\n")
    
    # Paso 1: El 'médium' escribe la petición
    entrada = input("Escribe la petición (empieza con '.' para truco): ")
    
    if entrada.startswith("."):
        # El resto del texto es la respuesta secreta
        respuesta_secreta = entrada[1:]
        visible, respuesta = mostrar_peticion(respuesta_secreta)
        print("\nEn pantalla aparece la petición:")
        print(f"> {visible}\n")
    else:
        print("Debes empezar con '.' para que funcione el truco.")
        return
    
    # Paso 2: La 'víctima' escribe la pregunta
    pregunta = input("Escribe tu pregunta: ")
    
    # Paso 3: Peter responde mágicamente
    print("\nPeter responde:")
    print(f"> {respuesta}")


if __name__ == "__main__":
    peter_answers()
