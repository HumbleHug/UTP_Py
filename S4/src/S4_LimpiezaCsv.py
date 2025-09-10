import csv
from datetime import datetime
from pathlib import Path
from statistics import mean     #de la paqueteria estadisticas importo promedio

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
    bad_ts = bad_val = 0    #para ver cuantos valores malos va a haber
    voltajes = []   #se crea una lista de voltajes
    for row in reader:
        total += 1  
        ts_raw = (row.get("timestamp") or "").strip()   #toma los valores de la columna timstamp en crudo (row) y elimina los vacios
        val_raw = (row.get("value") or "").strip()      #toma los valores de la columna valores en crudo (row) y elimina los vacios

#limpiar datos (voltajes)
        val_raw = val_raw.replace(",", ".")     #reemplaza , por .
        val_low = val_raw.lower() #convierte toda la cadena en minusculas para poder filtrarlo mejor
        if val_low in {"", "na", "n/a", "nan", "null", "none", "error"}:
            bad_ts += 1     #suma 1 a los valores malos
            continue  # saltar fila exceptuando los valores de arriba
        try:
            val = float(val_raw)    #nueva variable val, donde van a estar los row con valores limpios
        except ValueError:
            bad_ts += 1     #suma 1 a los valores malos
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
                bad_ts += 1     #suma 1 a los valores malos
                ts_clean = None

        if ts_clean is None:
            continue  #saltar fila si no pudimos interpretar la fecha

        if val >= 5:
            control = "CUIDADO"
        else:
            control = "OK"
        voltajes.append(val)
#grabar datos en writer
        writer.writerow({"Tiempo": ts_clean, "Voltaje": f"{val:.2f}", "Control": control})
        kept += 1 #sume 1 kept, en nuestro caso cambia de fila

print(f"La cantidad de voltajes limpios es: {len(voltajes)}")   #lee la cantidad de la lista voltajes
print(f"{min(voltajes):.2f}", f"{max(voltajes):.2f}", f"{mean(voltajes):.2f}")

#KPIs
n=len(voltajes)
if n==0:    #si n es 0 crea un kpi con los siguientes datos
    kpis={"n": 0, "min": None, "max": None, "prom": None, "alerts": 0, "alerts_pct": 0.0}     #formato de diccionario
else:
    alertas=sum(v >= 5 for v in voltajes)   #genera el caso contrario de los kpis
    kpis={
        'n': n,
        'min': min(voltajes),
        'max': max(voltajes),
        'prom': mean(voltajes),
        "alerts": alertas,
        "alerts_pct": 100.0 * alertas / n,
    }

#Calidad de los KPIS
descartes_totales = bad_ts + bad_val            # equivale a (total - kept) con esta lógica
pct_descartadas = (descartes_totales / total * 100.0) if total else 0.0
kpis_calidad = {
    "filas_totales": total,
    "filas_validas": kept,
    "descartes_timestamp": bad_ts,
    "descartes_valor": bad_val,
    "%descartadas": round(pct_descartadas, 2),
}
#Salida en pantalla y verificacion de KPIS
print(f'El archivo {IN_FILE} ha generado el archivo de salida {OUT_FILE}')
print(f'De un total de {int(kpis["n"])} datos, los valores maximo y minimo son: {float(kpis["max"]):.2f} V, {kpis["min"]} V')
print(kpis_calidad)