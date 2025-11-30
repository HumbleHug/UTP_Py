import sys
import csv
from pathlib import Path

# Agregar carpeta raíz
sys.path.append(str(Path(__file__).resolve().parent))

from src import (
    Root, ensure_dirs, list_raw_csvs, make_clean_name, safe_stem,
    clean_radar_file, kpis_radar,
    plot_radar_line, plot_radar_hist, plot_comparison_boxplot, plot_band_timeline, plot_band_distribution
    )


# === Configuración ===
ROOT = Root(__file__)
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"
PLOTS_DIR = ROOT / "plots"
REPORTS_DIR = ROOT / "reports"

ensure_dirs(RAW_DIR, PROC_DIR, PLOTS_DIR, REPORTS_DIR)

def main():
    raw_files = list_raw_csvs(RAW_DIR, pattern="*.csv")
    if not raw_files:
        print(f"⚠️ No hay CSVs en {RAW_DIR}. Sube 'data_normal.csv' y 'data_evento.csv'.")
        return

    resumen_kpis = []
    
    # Diccionario para acumular datos para el Boxplot Comparativo
    # Clave: Nombre del archivo (ej: 'data_normal'), Valor: Lista de distancias
    datos_para_boxplot = {} 

    print("--- Iniciando Análisis de Radar ---")

    for in_path in raw_files:
        print(f"Procesando: {in_path.name}...")
        
        # 1. Limpieza
        clean_name = make_clean_name(in_path)
        out_path = PROC_DIR / clean_name
        
        ts, dists, bandas, stats = clean_radar_file(in_path, out_path)
        
        if not ts:
            print(f"  -> Archivo vacío o inválido: {in_path.name}")
            continue

        # Guardar datos en memoria para el Boxplot final
        # Usamos in_path.stem (nombre sin extensión) como etiqueta
        datos_para_boxplot[in_path.stem] = dists

        # 2. KPIs individuales
        kv = kpis_radar(dists, bandas)
        
        row_report = {
            "archivo": in_path.name,
            **stats,
            **kv
        }
        resumen_kpis.append(row_report)

        # 3. Gráficos Individuales (Línea e Histograma)
        stem_safe = safe_stem(out_path)
        
        plot_radar_line(ts, dists, bandas, PLOTS_DIR / f"{stem_safe}_line.png")
        plot_radar_hist(dists, PLOTS_DIR / f"{stem_safe}_hist.png")
        plot_band_timeline(ts, bandas, out_path=PLOTS_DIR / f"{stem_safe}__timeline.png")
        plot_band_distribution(bandas, out_path=PLOTS_DIR / f"{stem_safe}__distribucion.png")

    # 4. Gráfico Comparativo (Boxplot)
    if len(datos_para_boxplot) > 0:
        print("Generando Boxplot Comparativo...")
        plot_comparison_boxplot(
            datos_para_boxplot, 
            out_path=PLOTS_DIR / "comparacion_escenarios_boxplot.png"
        )

    # 5. Guardar Reporte CSV
    if resumen_kpis:
        rep_csv = REPORTS_DIR / "kpis_radar.csv"
        keys = list(resumen_kpis[0].keys()) # Obtener columnas dinámicamente
        
        with rep_csv.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(resumen_kpis)
            
        print(f"Reporte generado en: {rep_csv}")
        print(f"Gráficos generados en: {PLOTS_DIR}")
    else:
        print("⚠️ No se generaron KPIs.")

if __name__ == "__main__":
    main()