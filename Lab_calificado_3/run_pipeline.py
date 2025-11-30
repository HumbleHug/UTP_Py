import sys
from pathlib import Path
# Agregar la carpeta raíz al path (donde está /src)
sys.path.append(str(Path(__file__).resolve().parent))

import csv
from src import (
    Root, ensure_dirs, list_raw_csvs, make_clean_name, safe_stem,
    clean_file, kpis_hum,
    plot_hum_line, plot_hum_hist
)

# === Parámetros ===
ROOT = Root(__file__)
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"
PLOTS_DIR = ROOT / "plots"
REPORTS_DIR = ROOT / "reports"

# === Umbrales para DHT22 (humedad %) ===
UMBRAL_ALERTA = 70.0  # ALERT_ON
UMBRAL_OFF = 68.0     # ALERT_OFF

ensure_dirs(RAW_DIR, PROC_DIR, PLOTS_DIR, REPORTS_DIR)

def main():
    raw_files = list_raw_csvs(RAW_DIR, pattern="*.csv")
    if not raw_files:
        print(f"No hay CSV en crudo en {RAW_DIR}")
        return

    resumen_kpis = []

    for in_path in raw_files:
        # Nombre de salida limpio
        clean_name = make_clean_name(in_path)
        out_path = PROC_DIR / clean_name

        # 1) Limpiar y escribir CSV limpio
        ts, vals, vals_avg, stats = clean_file(in_path, out_path)
        if not ts:
            print("Sin datos válidos:", in_path.name)
            continue

        # 2) KPIs por archivo
        kv = kpis_hum(vals, alert_on=UMBRAL_ALERTA, alert_off=UMBRAL_OFF)
        resumen_kpis.append({
            "archivo": in_path.name,
            "salida": out_path.name,
            **stats,  # calidad
            **kv
        })

        # 3) Gráficos por archivo
        stem_safe = safe_stem(out_path)
        plot_hum_line(
            ts, vals, UMBRAL_ALERTA,
            out_path=PLOTS_DIR / f"{stem_safe}__line.png"
        )
        plot_hum_hist(
            vals,
            out_path=PLOTS_DIR / f"{stem_safe}__hist.png",
            bins=15
        )

    # 4) Guardar reporte KPIs
    rep_csv = REPORTS_DIR / "kpis_por_archivo.csv"
    with rep_csv.open("w", encoding="utf-8", newline="") as f:
        cols = [
            "archivo", "salida", "filas_totales", "filas_validas",
            "descartes_valor", "descartes_valor_avg", "%descartadas",
            "n", "min", "max", "prom", "alerts_activadas", "alerts_pct"
        ]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in resumen_kpis:
            w.writerow(row)
    print("Reporte KPIs generado en:", rep_csv)


if __name__ == "__main__":
    main()


