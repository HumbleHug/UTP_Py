from pathlib import Path  #busca la ruta de los archivos

ROOT = Path(__file__).resolve().parents[0]  #busca la ruta, se corrobora con print
TXT = ROOT / "Archivos" / "mediciones_200_mixto.txt"   #dentro de archivos(carpeta) debe encontrar "mediciones_basico.txt"

#codigo de limpieza
valores=[]
with open(TXT, 'r', encoding="utf-8") as f:     #lee TXT con (r), enconding todo eso en una variable f
    for linea in f:     #linea por linea del archivo ingresado, linea es un v
        s=linea.strip()     #elimina las lineas en blanco del TXT
        if not s or s.startswith("#"):  #si lo primero que lee en la linea es "#" no lo toma y continua
            continue
        if not s or s.startswith("!"):  #si lo primero que lee en la linea es "!" no lo toma y continua
            continue
        s = s.strip()       # elimina espacios al inicio y final
        s = s.replace(",",".")  #reemplaza , por . y no salta datos
        try:
            valores.append(float(s))    #.append(float(s)) toma s, lo convierte en decimal y lo guarda en valores 
        except ValueError:
            #si no es ni linea ni numero, debe saltarlo
            pass
print(valores)

#codigo para mostrar en pantalla
Vmayor=[]
Vmenor=[]
for i in valores:
    if i >= 5:
        Vmayor.append(i)    #toma los datos mayores a 5 y los guarda en valores 
    else:
        Vmenor.append(i)    #toma los datos mayores a 5 y los guarda en valores 
print(Vmayor)
print(f"La cantidad de datos mayores son: {len(Vmayor)}")  #menciona la cantidad de datos (mediante el f-string)
print(Vmenor)
print(f"La cantidad de datos menores son: {len(Vmenor)}")  #menciona la cantidad de datos (mediante el f-string)