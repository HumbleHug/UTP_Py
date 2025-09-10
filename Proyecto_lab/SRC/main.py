from pathlib import Path
from defunct import (
    leer_csv,
    limpiar_datos,
    convertir_temp,
    marcar_alertas,
    calcular_kpis,
    guardar_csv
)

# rutas de entrada y salida
ROOT = Path(__file__).resolve().parents[1]
IN_FILE = ROOT / "DATA" / "RAW" / "datos_sucios_250_v2.csv"
OUT_FILE = ROOT / "DATA" / "PROCESSED" / "Temperaturas_Procesado.csv"

# flujo de trabajo
rows = leer_csv(IN_FILE)
voltajes, datos_limpios, total, kept, bad_ts, bad_val = limpiar_datos(rows)
datos_limpios = convertir_temp(datos_limpios)
datos_limpios = marcar_alertas(datos_limpios)

kpis = calcular_kpis(voltajes, total, kept, bad_ts, bad_val, datos_limpios)
guardar_csv(OUT_FILE, datos_limpios)

# impresión final de KPIs
print("=== KPIs ===")
print(f"Filas_totales: {kpis['Filas_totales']}")
print(f"Filas_validas: {kpis['Filas_validas']}")
print(f"Descartes_Timestamp: {kpis['Descartes_Timestamp']}")
print(f"Descartes_valor: {kpis['Descartes_valor']}")
print(f"n: {kpis['n']}")
print(f"Temp_min: {kpis['temp_min']:.2f}" if kpis['temp_min'] is not None else "Temp_min: None")
print(f"Temp_max: {kpis['temp_max']:.2f}" if kpis['temp_max'] is not None else "Temp_max: None")
print(f"Temp_prom: {kpis['temp_prom']:.2f}" if kpis['temp_prom'] is not None else "Temp_prom: None")
print(f"Alertas: {kpis['Alertas']}")