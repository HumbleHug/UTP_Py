import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def plot_hum_line(ts, hums, umbral_h: float, out_path: Path):           # Gráfico de línea
    plt.figure(figsize=(9, 4))
    plt.plot(ts, hums, label="Humedad (%)", color="blue")
    alerts_t = [t for t, h in zip(ts, hums) if h > umbral_h]
    alerts_h = [h for h in hums if h > umbral_h]
    plt.scatter(alerts_t, alerts_h, color="red", s=20, label=f"Alertas (> {umbral_h}%)")
    plt.axhline(umbral_h, color="r", linestyle="--", label=f"Umbral {umbral_h}%")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.title("Humedad vs Tiempo - datos_sensor.csv")
    plt.xlabel("Tiempo")
    plt.ylabel("Humedad (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.show()


def plot_hum_hist(hums, out_path: Path, bins: int = 20):            # Histograma
    plt.figure(figsize=(6, 4))
    plt.hist(hums, bins=bins, color="skyblue", edgecolor="black")
    plt.title("Histograma de Humedad - datos_sensor.csv")
    plt.xlabel("Humedad (%)")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.show()