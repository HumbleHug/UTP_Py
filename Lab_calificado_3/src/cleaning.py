import csv
from datetime import datetime
from pathlib import Path
from .IO_Utils import detectar_delimitador

# Detecta y marca como inválidos los valores vacíos
NA_TOKENS = {"", "na", "n/a", "nan", "null", "none", "error"}

def parse_v(s: str):
    """Convierte a float, admitiendo coma decimal y tokens NA."""
    if s is None:
        return None
    s = str(s).strip().replace(",", ".").lower()
    if s in NA_TOKENS:
        return None
    try:
        return float(s)
    except ValueError:
        return None

def clean_file(in_path: Path, out_path: Path):
    """
    Lee un CSV crudo de humedad, limpia y escribe un CSV con encabezado:
    ts_ms, humedad, humedad_avg, estado
    Devuelve: (ts_list, humedades, promedios, stats)
    """
    delim = detectar_delimitador(in_path)
    total = kept = bad_val = bad_avg = 0
    ts_list, humedades, promedios = [], [], []  #nombres claros

    with in_path.open("r", encoding="utf-8", newline="") as fin, \
         out_path.open("w", encoding="utf-8", newline="") as fout:
        reader = csv.DictReader(fin, delimiter=delim)
        writer = csv.DictWriter(
            fout, fieldnames=["ts_ms", "humedad", "humedad_avg", "estado"]  #nombres actualizados
        )
        writer.writeheader()

        for row in reader:
            total += 1
            try:
                ts = int(row.get("ts_ms", "").strip())
            except ValueError:
                continue

            v = parse_v(row.get("valor"))       #'valor' = humedad instantánea
            v_avg = parse_v(row.get("valor_avg"))  #'valor_avg' = humedad promedio
            estado = row.get("estado", "UNKNOWN").strip()

            if v is None:
                bad_val += 1
                continue
            if v_avg is None:
                bad_avg += 1
                continue

            writer.writerow({
                "ts_ms": ts,
                "humedad": f"{v:.3f}",
                "humedad_avg": f"{v_avg:.3f}",
                "estado": estado
            })

            ts_list.append(ts)
            humedades.append(v)
            promedios.append(v_avg)
            kept += 1

    stats = {
        "filas_totales": total,
        "filas_validas": kept,
        "descartes_valor": bad_val,
        "descartes_valor_avg": bad_avg,
        "%descartadas": round(((bad_val + bad_avg) / total * 100.0) if total else 0.0, 2),
    }

    return ts_list, humedades, promedios, stats  #variables con nombres semánticos