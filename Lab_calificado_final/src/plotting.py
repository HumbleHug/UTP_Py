import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta

def format_ts(ts_list_ms):
    """Convierte ms relativos a objetos datetime arbitrarios para graficar eje X bonito."""
    base_time = datetime(2023, 1, 1, 12, 0, 0) # Fecha ficticia
    return [base_time + timedelta(milliseconds=t) for t in ts_list_ms]

def plot_radar_line(ts_ms, dists, bandas, out_path: Path):
    """Línea temporal de distancia, filtrando UNKNOWN y usando colores de umbral."""
    dates = format_ts(ts_ms)
    
    plt.figure(figsize=(10, 5))
    
    # 1. Graficamos la trayectoria base en gris
    plt.plot(dates, dists, color="gray", alpha=0.5, label="Trayectoria", zorder=1)
    
    # Mapeo de nombres del CSV (Inglés) a nombres de Leyenda/Color (Español)
    # 🛑 CAMBIO CLAVE: Usamos CLOSE en lugar de MID
    banda_map = {
        "CLOSE": "CERCA",  # Nuevo estado para la zona más cercana
        "NEAR": "INTERMEDIO", # Mapeamos NEAR a INTERMEDIO (o puedes dejarlo como "NEAR")
        "FAR": "LEJOS",
    }
    
    # Colores definidos
    colors = {
        "CERCA": "red", 
        "INTERMEDIO": "orange", 
        "LEJOS": "green"
    }
    
    # --- 2. Preparación de datos para Scatter (Solo Puntos Válidos) ---
    valid_dates = []
    valid_dists = []
    color_list = []
    bandas_presentes = set() 
    
    for i, b_original in enumerate(bandas):
        b_upper = b_original.upper() 
        
        # Intentar mapear el nombre a español
        banda_estandarizada = banda_map.get(b_upper) 
        
        # Solo pintar y registrar si el mapeo fue exitoso y el color existe
        if banda_estandarizada and banda_estandarizada in colors:
            valid_dates.append(dates[i])
            valid_dists.append(dists[i])
            color_list.append(colors[banda_estandarizada])
            bandas_presentes.add(banda_estandarizada)
            
    # 3. Graficamos solo los puntos válidos
    plt.scatter(valid_dates, valid_dists, c=color_list, s=15, zorder=2)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%M:%S"))
    plt.title(f"Radar HC-SR04: Distancia vs Tiempo ({out_path.stem.replace('_limpio_line', '')})")
    plt.ylabel("Distancia (cm)")
    plt.xlabel("Tiempo (min:seg)")
    plt.grid(True, linestyle="--", alpha=0.7)
    
    # --- 4. Creación de Leyenda ---
    legend_elements = []
    # Ordenamos las bandas: CLOSE -> NEAR -> FAR
    orden_bandas = ["CERCA", "INTERMEDIO", "LEJOS"] 
    
    for b_name in orden_bandas:
        if b_name in bandas_presentes: 
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                              label=b_name, 
                                              markerfacecolor=colors[b_name], 
                                              markersize=8))
    
    plt.legend(handles=legend_elements, title="Bandas")
    
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120)
    plt.close()

def plot_radar_hist(dists, out_path: Path):
    plt.figure(figsize=(6, 4))
    plt.hist(dists, bins=20, color="purple", alpha=0.7, edgecolor="black")
    plt.title(f"Distribución de Distancias ({out_path.stem})")
    plt.xlabel("Distancia (cm)")
    plt.ylabel("Frecuencia")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.close()

def plot_comparison_boxplot(data_dict, out_path: Path):
    """
    Genera un Boxplot comparando múltiples archivos.
    data_dict: {"NombreArchivo": [lista_distancias], ...}
    """
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(8, 6))
    # Boxplot sin pandas
    plt.boxplot(values, labels=labels, patch_artist=True, 
                boxprops=dict(facecolor="lightblue"))
    
    plt.title("Comparación de Escenarios: Distribución de Distancia")
    plt.ylabel("Distancia (cm)")
    plt.grid(True, axis='y', linestyle='--')
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120)
    plt.close()