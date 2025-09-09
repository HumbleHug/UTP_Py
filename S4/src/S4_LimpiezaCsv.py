import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]      #se declara en mayusculas porque son constantes
IN_FILE = ROOT / "raw" / "voltajes_250_sucio.csv"   #entra a la carpeta raw y busca el archivo
OUT_FILE = ROOT / "processing" / "voltajes_250_limpio.csv"  #entra a la carpeta proccesing y da el .csv limpio

#apertura de archivos
with open(IN_FILE, 'r', encoding="utf-8", newline="") as fin,\
    open(OUT_FILE, 'w', encoding="utf-8", newline="") as fout: 
    reader = csv.DictReader(fin, delimiter=';')     #delimitador ; se puede cambiar por otro en el csv; porque es lo que separa las columnas
    writer = csv.DictWriter(fout, fieldnames=["Tiempo", "Voltaje", "Control"])    #crea el archivo con las cabeceras que se coloquen
    writer.writeheader()
#leer linea por linea y seleccionar en crudo raw/row
    total = kept = 0
    for row in reader:
        total += 1
        ts_raw = (row.get("timestamp") or "").strip()   #toma los valores de la columna timstamp en crudo (row) y elimina los vacios
        val_raw = (row.get("value") or "").strip()      #toma los valores de la columna valores en crudo (row) y elimina los vacios

#limpiar datos (voltajes)
        val_raw = val_raw.replace(",", ".")     #reemplaza , por .
        val_low = val_raw.lower() #convierte toda la cadena en minusculas para poder filtrarlo mejor
        if val_low in {"", "na", "n/a", "nan", "null", "none", "error"}:
            continue  # saltar fila exceptuando los valores de arriba
        try:
            val = float(val_raw)    #nueva variable val, donde van a estar los row con valores limpios
        except ValueError:
            continue  # saltar fila si no es número

#limpieza de datos de tiempo (copia y pega nomas)
        ts_clean = None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
            try:
                dt = datetime.strptime(ts_raw, fmt)
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
                break
            except ValueError:
                pass

#milisegundo (opcional)
        if ts_clean is None and "T" in ts_raw and len(ts_raw) >= 19:
            try:
                dt = datetime.strptime(ts_raw[:19], "%Y-%m-%dT%H:%M:%S")
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except ValueError:
                ts_clean = None

        if ts_clean is None:
            continue  #saltar fila si no pudimos interpretar la fecha

        if val >= 5:
            control = "CUIDADO"
        else:
            control = "OK"

#grabar datos en writer
        writer.writerow({"Tiempo": ts_clean, "Voltaje": f"{val:.2f}", "Control": control})
        kept += 1 #sume 1 kept, en nuestro caso cambia de fila