import csv
from pathlib import Path
from .IO_Utils import detectar_delimitador

NA_TOKENS = {"", "na", "nan", "null", "none"}

def parse_float(s: str):
    """Convierte string a float asegurando punto decimal."""
    if s is None: return None
    s = str(s).strip().replace(",", ".").lower()
    if s in NA_TOKENS: return None
    try:
        return float(s)
    except ValueError:
        return None

def clean_radar_file(in_path: Path, out_path: Path):
    """
    Lee CSV del Radar: ts_ms; sensor_id; valor_cm; valor_avg; estado_id; estado_nombre
    Genera CSV limpio: ts_ms, distancia, banda
    Devuelve: (ts_list, distancias, bandas_list, stats)
    """
    delim = detectar_delimitador(in_path)
    total = kept = bad_val = 0
    
    ts_list, dists, bandas = [], [], []

    with in_path.open("r", encoding="utf-8", newline="") as fin, \
         out_path.open("w", encoding="utf-8", newline="") as fout:
        
        # Leemos con DictReader. OJO: strip() en nombres de columnas por si hay espacios
        reader = csv.DictReader(fin, delimiter=delim)
        reader.fieldnames = [f.strip() for f in reader.fieldnames] 

        writer = csv.DictWriter(fout, fieldnames=["ts_ms", "distancia", "banda"])
        writer.writeheader()

        for row in reader:
            total += 1
            # 1. Parsear Tiempo
            try:
                ts = int(row.get("ts_ms", "").strip())
            except ValueError:
                continue

            # 2. Parsear Distancia (valor_cm)
            raw_val = row.get("valor_cm", "")
            dist = parse_float(raw_val)

            # 3. Obtener Banda (estado_nombre)
            banda = row.get("estado_nombre", "UNKNOWN").strip()

            if dist is None:
                bad_val += 1
                continue

            # Escribir fila limpia
            writer.writerow({
                "ts_ms": ts,
                "distancia": f"{dist:.2f}",
                "banda": banda
            })

            ts_list.append(ts)
            dists.append(dist)
            bandas.append(banda)
            kept += 1

    stats = {
        "filas_totales": total,
        "filas_validas": kept,
        "descartes": bad_val,
        "%descartadas": round((bad_val / total * 100.0) if total else 0.0, 2),
    }

    return ts_list, dists, bandas, stats