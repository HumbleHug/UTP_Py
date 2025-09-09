import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TXT = ROOT / "Repositorio Python"
IN_FILE = Path(r"C:\Users\OSCAR LOPEZ\Documents\Repositorio Python\voltajes_250_sucio.csv")
OUT_FILE = Path(r"C:\Users\OSCAR LOPEZ\Documents\Repositorio Python\voltajes_250_limpio.csv")
#apertura de archivos
with open(IN_FILE, 'r', encoding="utf-8", newline="") as fin,\
    open(OUT_FILE, 'w', encoding="utf-8", newline="") as fout: 
    reader = csv.DictReader(fin, delimiter=';')
    writer = csv.DictWriter(fout, fieldnames=["timestamp", "value"])
    writer.writeheader()
#leer linea por linea y seleccionar en crudo raw
    total = kept = 0
    for row in reader:
        total += 1
        ts_raw = (row.get("timestamp") or "").strip() #toma los valores de la columnas timstamp
        val_raw = (row.get("value") or "").strip() 
#limpiar datos
        val_raw = val_raw.replace(",", ".")
        val_low = val_raw.lower() #empezar a eliminar los valores no existentes
        if val_low in {"", "na", "n/a", "nan", "null", "none", "error"}:
            continue  # saltar fila
        try:
            val = float(val_raw)
        except ValueError:
            continue  # saltar fila si no es número
#limpieza de datos de tiempo 
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
            continue  # saltar fila si no pudimos interpretar la fecha

        if val >= 5:
            control = "CUIDADO"
        else:
            control = "OK"

#grabar datos en writer
        writer.writerow({"timestamp": ts_clean, "value": f"{val:.2f}"})
        kept += 1 #sume 1 kept, en nuestro caso cambia de fila