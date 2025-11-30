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

def plot_band_timeline(ts_ms, bandas, out_path: Path):
    """
    Genera un timeline escalonado que muestra la banda activa (0, 1, 2)
    a lo largo del tiempo.
    """
    dates = format_ts(ts_ms)
    
    # Mapeo de estados de banda a valores enteros
    banda_to_int = {
        "CLOSE": 0,
        "NEAR": 1,
        "FAR": 2,
    }
    
    # Etiquetas que aparecerán en el eje Y
    banda_labels = {
        0: "CERCA (CLOSE)",
        1: "INTERMEDIO (NEAR)",
        2: "LEJOS (FAR)",
    }
    
    int_bands = []
    
    # Convertimos la lista de bandas a una lista de enteros
    for b_original in bandas:
        b_upper = b_original.upper()
        # Usamos .get() para asignar -1 (un valor no ploteable) si es desconocido
        int_bands.append(banda_to_int.get(b_upper, -1)) 
        
    # --- Generación del Gráfico ---
    plt.figure(figsize=(10, 3.5))
    
    # Usamos plt.step para generar la gráfica escalonada (timeline)
    # Excluimos los valores -1 (UNKNOWN)
    valid_indices = [i for i, b in enumerate(int_bands) if b != -1]
    
    # Filtramos las listas para solo incluir los datos válidos
    valid_dates = [dates[i] for i in valid_indices]
    valid_int_bands = [int_bands[i] for i in valid_indices]
    
    if valid_dates:
        # El estilo 'post' asegura que la línea se dibuje horizontalmente hasta el siguiente punto.
        plt.step(valid_dates, valid_int_bands, where='post', color='darkorange', alpha=0.8, linewidth=2)
    
    # 1. Configuración del Eje Y
    # Configuramos el eje Y para que muestre 0, 1, 2
    plt.yticks(list(banda_labels.keys()), list(banda_labels.values()))
    plt.ylim(-0.5, 2.5) # Rango para centrar los valores 0, 1, 2
    
    # 2. Configuración del Eje X
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%M:%S"))
    
    plt.title(f"Timeline de Banda del Radar ({out_path.stem.replace('_limpio_timeline', '')})")
    plt.xlabel("Tiempo (min:seg)")
    plt.ylabel("Banda Activa")
    plt.grid(True, axis='x', linestyle='--', alpha=0.6) # Solo grid vertical
    plt.tight_layout()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120)
    plt.close()

def plot_band_distribution(bandas, out_path: Path):
    """
    Genera un gráfico de barras horizontales que muestra la frecuencia de cada banda.
    bandas: Lista de strings con los estados (ej. ['FAR', 'NEAR', 'NEAR', 'FAR', ...])
    """
    
    # 1. Conteo y Normalización (Similar a lo que hace kpis.py)
    conteo = {}
    total_samples = len(bandas)
    
    # Mapeo a español para etiquetas
    banda_map = {
        "CLOSE": "CERCA",
        "NEAR": "INTERMEDIO",
        "FAR": "LEJOS",
    }
    
    # Contar solo las bandas conocidas y normalizarlas
    for b_original in bandas:
        b_upper = b_original.upper()
        banda_std = banda_map.get(b_upper)
        if banda_std:
            conteo[banda_std] = conteo.get(banda_std, 0) + 1
    
    if not conteo:
        print(f"Advertencia: No hay datos válidos (CLOSE, NEAR, FAR) para la distribución en {out_path.stem}.")
        return

    # Preparar datos para la gráfica (ordenando las barras)
    etiquetas = []
    porcentajes = []
    
    # Ordenar de CERCA a LEJOS (CLOSE, NEAR, FAR)
    orden = ["CERCA", "INTERMEDIO", "LEJOS"]
    colores = {"CERCA": "red", "INTERMEDIO": "orange", "LEJOS": "green"}
    
    for banda_nombre in orden:
        if banda_nombre in conteo:
            porc = 100 * conteo[banda_nombre] / total_samples
            etiquetas.append(f"{banda_nombre} ({conteo[banda_nombre]} muestras)")
            porcentajes.append(porc)

    # --- 2. Generación del Gráfico ---
    plt.figure(figsize=(7, 4))
    
    # Graficar las barras horizontalmente (barh)
    barras = plt.barh(etiquetas, porcentajes, 
                      color=[colores[e.split(' ')[0]] for e in etiquetas])
    
    # Añadir texto con el porcentaje en cada barra
    for bar in barras:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, 
                 f'{width:.1f}%',
                 va='center', ha='left', fontsize=9)

    plt.title(f"Distribución Porcentual de Bandas ({out_path.stem.replace('_limpio', '')})")
    plt.xlabel("Porcentaje de Tiempo (%)")
    plt.xlim(0, 105) # Rango ligeramente superior a 100% para el texto
    plt.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=120)
    plt.close()