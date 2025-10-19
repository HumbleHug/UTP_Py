from statistics import mean

def kpis_volt(temp, umbral=80.0):
    """KPIs de temperatura: n, min, max, prom, alertas y %."""
    temp = [float(v) for v in temp if v is not None]
    n = len(temp)
    if n == 0:
        return {"n":0,"min":None,"max":None,"prom":None,"alerts":0,"alerts_pct":0.0}
    alerts = sum(v > umbral for v in temp)
    return {
        "n": n,
        "min": round(min(temp), 2),
        "max": round(max(temp), 2),
        "prom": round(mean(temp), 2),
        "alerts": alerts,
        "alerts_pct": round(100.0 * alerts / n, 2)
    }