from statistics import mean

def kpis_hum(valores, alert_on=70.0, alert_off=68.0):
    """KPIs de humedad: cantidad de muestras, min, max, promedio, alertas y porcentaje en alerta."""
    valores = [float(v) for v in valores if v is not None]
    n = len(valores)
    if n == 0:
        return {
            "n": 0,
            "min": None,
            "max": None,
            "prom": None,
            "alerts_activadas": 0,
            "alerts_pct": 0.0,
        }

    # Detecta entradas y salidas del estado de alerta según los umbrales definidos
    en_alerta = False
    alertas = 0

    for v in valores:
        if not en_alerta and v >= alert_on:     # Se activa una nueva alerta
            en_alerta = True
            alertas += 1
        elif en_alerta and v <= alert_off:      # Se desactiva la alerta
            en_alerta = False

    return {
        "n": n,
        "min": round(min(valores), 2),
        "max": round(max(valores), 2),
        "prom": round(mean(valores), 2),
        "alerts_activadas": alertas,
        "alerts_pct": round(100.0 * sum(v >= alert_on for v in valores) / n, 2),
    }

