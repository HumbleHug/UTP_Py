import csv
from pathlib import Path
from datetime import datetime
from statistics import mean

# rutas de entrada y salida
ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / "DATA" / "RAW" / "datos_sucios_250_v2.csv"
OUT_FILE = ROOT / "DATA" / "PROCESSED" / "Temperaturas_Procesado.csv"

#Leer
def leer_csv(in_file):
    with open(in_file, 'r', encoding="utf-8", newline="") as fin:
        reader = csv.DictReader(fin, delimiter=';')
        return list(reader)

#Limpiar datos
def limpiar_datos(rows):
    voltajes = []
    datos_limpios = []
    total = kept = 0
    bad_ts = bad_val = 0
    for row in rows:
        total += 1
        ts_raw = (row.get("timestamp") or "").strip()
        val_raw = (row.get("value") or "").strip()

        # limpiar valor
        val_raw = val_raw.replace(",", ".")
        val_low = val_raw.lower()
        if val_low in {"", "na", "n/a", "nan", "null", "none", "error"}:
            bad_val += 1
            continue
        try:
            val = float(val_raw)
        except ValueError:
            bad_val += 1
            continue

        # limpiar timestamp
        ts_clean = None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
            try:
                dt = datetime.strptime(ts_raw, fmt)
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
                break
            except ValueError:
                pass

        if ts_clean is None and "T" in ts_raw and len(ts_raw) >= 19:
            try:
                dt = datetime.strptime(ts_raw[:19], "%Y-%m-%dT%H:%M:%S")
                ts_clean = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except ValueError:
                bad_ts += 1
                ts_clean = None

        if ts_clean is None:
            continue

        voltajes.append(val)
        datos_limpios.append({"Timestamp": ts_clean, "Voltaje": val})
        kept += 1
    return voltajes, datos_limpios, total, kept, bad_ts, bad_val

# Convertir
def convertir_temp(datos_limpios):
    for row in datos_limpios:
        row["Temp_C"] = 18 * row["Voltaje"] - 64
    return datos_limpios

# Marcar alertas 
def marcar_alertas(datos_limpios):
    for row in datos_limpios:
        if row["Temp_C"] > 40:
            row["Alertas"] = "ALERTA"
        else:
            row["Alertas"] = "OK"
    return datos_limpios

# Calcular KPIs
def calcular_kpis(voltajes, total, kept, bad_ts, bad_val, datos_limpios):
    n = len(voltajes)
    if n == 0:
        kpis = {
            "Filas_totales": total,
            "Filas_validas": kept,
            "Descartes_Timestamp": bad_ts,
            "Descartes_valor": bad_val,
            "n": 0,
            "temp_min": None,
            "temp_max": None,
            "temp_prom": None,
            "Alertas": 0
        }
    else:
        temps = [row["Temp_C"] for row in datos_limpios]
        alertas = sum(t > 40 for t in temps)
        kpis = {
            "Filas_totales": total,
            "Filas_validas": kept,
            "Descartes_Timestamp": bad_ts,
            "Descartes_valor": bad_val,
            "n": n,
            "temp_min": min(temps),
            "temp_max": max(temps),
            "temp_prom": mean(temps),
            "Alertas": alertas
        }
    return kpis

# 6. Guardar CSV final
def guardar_csv(out_file, datos_limpios):
    with open(out_file, 'w', encoding="utf-8", newline="") as fout:
        encabezado = ["Timestamp", "Voltaje", "Temp_C", "Alertas"]
        writer = csv.DictWriter(fout, fieldnames=encabezado)
        writer.writeheader()
        for row in datos_limpios:
            writer.writerow({
                "Timestamp": row["Timestamp"], 
                "Voltaje": f"{row['Voltaje']:.2f}", 
                "Temp_C": f"{row['Temp_C']:.2f}", 
                "Alertas": row["Alertas"],
            })