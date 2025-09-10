import csv
from datetime import datetime
from statistics import mean

# -------------------
# 1. Leer CSV
# -------------------
def leer_csv(in_file):
    with open(in_file, 'r', encoding="utf-8", newline="") as fin:
        reader = csv.DictReader(fin, delimiter=';')
        return list(reader)


# -------------------
# 2. Limpiar datos
# -------------------
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
        datos_limpios.append({"Tiempo": ts_clean, "Voltaje": val})
        kept += 1

    return voltajes, datos_limpios, total, kept, bad_ts, bad_val


# -------------------
# 3. Conversión V → °C
# -------------------
def convertir_temp(datos_limpios):
    for row in datos_limpios:
        v = row["Voltaje"]
        row["TempC"] = 18 * v - 64
    return datos_limpios


# -------------------
# 4. Marcar alertas (> 40 °C)
# -------------------
def marcar_alertas(datos_limpios):
    for row in datos_limpios:
        row["Control"] = "ALERTA" if row["TempC"] > 40 else "OK"
    return datos_limpios


# -------------------
# 5. Calcular KPIs
# -------------------
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
        temps = [row["TempC"] for row in datos_limpios]
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


# -------------------
# 6. Guardar CSV final
# -------------------
def guardar_csv(out_file, datos_limpios):
    with open(out_file, 'w', encoding="utf-8", newline="") as fout:
        fieldnames = ["Tiempo", "Voltaje", "TempC", "Control"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in datos_limpios:
            writer.writerow({
                "Tiempo": row["Tiempo"],
                "Voltaje": f"{row['Voltaje']:.2f}",
                "TempC": f"{row['TempC']:.2f}",
                "Control": row["Control"],
            })