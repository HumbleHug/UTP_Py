from defunct import (
    IN_FILE,
    OUT_FILE,
    leer_csv,
    limpiar_datos,
    convertir_temp,
    marcar_alertas,
    calcular_kpis,
    guardar_csv
)

def main():
    # flujo de trabajo
    rows = leer_csv(IN_FILE)
    voltajes, datos_limpios, total, kept, bad_ts, bad_val = limpiar_datos(rows)
    datos_limpios = convertir_temp(datos_limpios)
    datos_limpios = marcar_alertas(datos_limpios)

    kpis = calcular_kpis(voltajes, total, kept, bad_ts, bad_val, datos_limpios)
    guardar_csv(OUT_FILE, datos_limpios)

    # impresión final de KPIs
    print("=== KPIs ===")
    for k, v in kpis.items():
        if isinstance(v, float):
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()