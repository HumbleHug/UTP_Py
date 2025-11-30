from statistics import mean

def kpis_radar(distancias, bandas):
    """
    KPIs Radar: 
    - Estadísticos de distancia (min, max, mean).
    - Distribución de bandas (% tiempo en cada zona).
    - Saltos de banda (cantidad de transiciones).
    """
    if not distancias:
        return {"n": 0}

    n = len(distancias)
    
    # 1. Estadísticos básicos
    d_min = min(distancias)
    d_max = max(distancias)
    d_avg = mean(distancias)

    # 2. Conteo de Bandas (Distribución)
    # Ejemplo bandas: "LEJOS", "MEDIO", "CERCA"
    conteo_bandas = {}
    for b in bandas:
        conteo_bandas[b] = conteo_bandas.get(b, 0) + 1
    
    # Convertir a porcentajes
    distribucion_str = " | ".join(
        [f"{k}: {v/n*100:.1f}%" for k, v in conteo_bandas.items()]
    )

    # 3. Saltos de Banda (Estabilidad)
    # Cuenta cuántas veces cambia el estado respecto al anterior
    saltos = 0
    for i in range(1, n):
        if bandas[i] != bandas[i-1]:
            saltos += 1

    return {
        "n": n,
        "min_cm": round(d_min, 2),
        "max_cm": round(d_max, 2),
        "avg_cm": round(d_avg, 2),
        "saltos_banda": saltos,       # KPI de estabilidad
        "distribucion_bandas": distribucion_str # KPI de ocupación
    }