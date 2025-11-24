import os 
import requests 
import numpy as np 
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt 
from scipy.signal import welch, find_peaks 
import pyedflib 

# 1. Configuración 
PACIENTE = "chb21" 
CANALES = ["FP1-F7", "FP2-F8"] 
FS = 256  # Frecuencia de muestreo 
DURACION = 2  # segundos 
URL_BASE = "https://physionet.org/files/chbmit/1.0.0/" 

# 2. Descargar archivo EDF 
def descargar_datos(): 
    os.makedirs("data", exist_ok=True) 
    archivo_edf = f"{PACIENTE}_01.edf" 
    ruta_archivo = f"data/{archivo_edf}"
    
    # --- Si el archivo existe, lo eliminamos para forzar una descarga completa ---
    if os.path.exists(ruta_archivo):
        print(f"Detectado archivo existente ({ruta_archivo}). Eliminando para forzar una nueva descarga completa (el anterior estaba corrupto).")
        os.remove(ruta_archivo)

    # Ahora procedemos a la descarga
    print(f"Descargando archivo {archivo_edf} desde {URL_BASE}{PACIENTE}/...") 
    url = f"{URL_BASE}{PACIENTE}/{archivo_edf}" 
    try: 
        response = requests.get(url, stream=True) 
        response.raise_for_status() # Lanza un error para códigos de estado 4xx/5xx
        with open(ruta_archivo, 'wb') as f: 
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk) 
        print(f"Descarga completada. Archivo guardado en {ruta_archivo}") 
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP al descargar: El archivo podría no existir en la URL. {e}")
        raise
    except Exception as e: 
        print(f"Error general al descargar: {e}") 
        raise 
 
 
# 3. Generar EEG normal simulado 
def generar_eeg_sano(duracion): 
    t = np.arange(0, duracion, 1/FS) 
    # Componentes rítmicas 
    alpha = 40 * np.sin(2 * np.pi * 10 * t)  # Ritmo alpha (10 Hz) 
    beta = 20 * np.sin(2 * np.pi * 20 * t)   # Ritmo beta (20 Hz) 
    # Ruido fisiológico simulado 
    theta = 15 * np.sin(2 * np.pi * 5 * t)   # Ritmo theta (5 Hz) 
    ruido = np.random.normal(0, 8, len(t))    # Ruido blanco 
    return alpha + beta + theta + ruido 
 
# 4. Cargar datos reales del paciente 
def cargar_datos_paciente(): 
    archivo_edf = f"data/{PACIENTE}_01.edf" 
    try: 
        with pyedflib.EdfReader(archivo_edf) as f: 
            print(f"Canales disponibles: {f.getSignalLabels()}") 
            indices = [f.getSignalLabels().index(c) for c in CANALES] 
            señales = [f.readSignal(i)[:FS*DURACION] for i in indices] 
        return np.array(señales) 
    except Exception as e: 
        print(f"Error al leer archivo EDF: {e}") 
        # Esta excepción será capturada por la función main()
        raise
 
# 5. Visualización con detección de picos 
def visualizar_comparacion(sano, paciente): 
    t = np.arange(0, DURACION, 1/FS) 
 
    # Configuración de estilo 
    plt.style.use('seaborn-v0_8') 
    plt.rcParams['figure.facecolor'] = 'white' 
    plt.rcParams['axes.grid'] = True 
    plt.rcParams['grid.alpha'] = 0.3 
 
    for i, canal in enumerate(CANALES): 
        fig, axs = plt.subplots(2, 2, figsize=(16, 12)) 
        fig.suptitle(f'Análisis de Picos EEG - Canal {canal}', fontsize=16, y=1.02) 
 
        # --- Parámetros de detección --- 
        eeg_prominence = 15  # μV (para evitar ruido) 
        fft_prominence = 2   # μV²/Hz 
 
        # --- 1. EEG Normal --- 
        ax = axs[0, 0] 
        ax.plot(t, sano[i], color='#3498db', linewidth=1.5, alpha=0.8, label='Señal') 
 
        # Detectar picos 
        peaks, properties = find_peaks(sano[i], prominence=eeg_prominence) 
 
        # Marcar picos 
        ax.plot(t[peaks], sano[i][peaks], "o", color='#e74c3c', markersize=8, 
                label=f'Picos ({len(peaks)})') 
 
        # Anotar los 3 picos más altos 
        if len(peaks) > 0: 
            top_3 = peaks[np.argsort(sano[i][peaks])[-3:]] 
            for p in top_3: 
                ax.annotate(f'{sano[i][p]:.1f}μV\n{t[p]:.2f}s', 
                            (t[p], sano[i][p]), 
                            textcoords="offset points", xytext=(0,10), 
                            ha='center', fontsize=9, 
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.set_title('EEG Normal Simulado', fontsize=14) 
        ax.set_xlabel('Tiempo (s)', fontsize=12) 
        ax.set_ylabel('Amplitud (μV)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        # --- 2. EEG Paciente --- 
        ax = axs[0, 1] 
        ax.plot(t, paciente[i], color='#9b59b6', linewidth=1.5, alpha=0.8, label='Señal') 
 
        # Detectar picos con menor distancia para capturar actividad epiléptica 
        peaks, _ = find_peaks(paciente[i], prominence=eeg_prominence, 
                              distance=int(FS*0.05)) 
 
        # Marcar picos (mostrar solo los 5 más prominentes para claridad) 
        ax.plot(t[peaks], paciente[i][peaks], "o", color='#e74c3c', markersize=8, 
                label=f'Picos ({len(peaks)})') 
 
        if len(peaks) > 0: 
            top_5 = peaks[np.argsort(paciente[i][peaks])[-5:]] 
            for p in top_5: 
                ax.annotate(f'{paciente[i][p]:.1f}μV\n{t[p]:.2f}s', 
                            (t[p], paciente[i][p]), 
                            textcoords="offset points", xytext=(0,10), 
                            ha='center', fontsize=9, 
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.set_title('EEG Paciente con Hipsarritmia', fontsize=14) 
        ax.set_xlabel('Tiempo (s)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        # --- 3. FFT Normal --- 
        ax = axs[1, 0] 
        f, Pxx = welch(sano[i], FS, nperseg=1024) 
        ax.plot(f, Pxx, color='#3498db', linewidth=1.5, alpha=0.8) 
 
        # Detectar picos en FFT 
        peaks, _ = find_peaks(Pxx, prominence=fft_prominence) 
 
        # Mostrar picos significativos (frecuencia < 40 Hz) 
        mask = f[peaks] <= 40 
        peaks = peaks[mask] 
 
        ax.plot(f[peaks], Pxx[peaks], "o", color='#e74c3c', markersize=8, 
                label=f'Picos ({len(peaks)})') 
 
        # Anotar frecuencias importantes 
        for j, p in enumerate(peaks): 
            if j < 3:  # Mostrar solo las 3 frecuencias principales 
                ax.annotate(f'{f[p]:.1f}Hz\n{Pxx[p]:.1f}', 
                            (f[p], Pxx[p]), 
                            textcoords="offset points", xytext=(0,10), 
                            ha='center', fontsize=9, 
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.set_xlim(0, 40) 
        ax.set_title('Espectro de Potencia - Normal', fontsize=14) 
        ax.set_xlabel('Frecuencia (Hz)', fontsize=12) 
        ax.set_ylabel('Densidad de Potencia (μV²/Hz)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        # --- 4. FFT Paciente --- 
        ax = axs[1, 1] 
        f, Pxx = welch(paciente[i], FS, nperseg=1024) 
        ax.plot(f, Pxx, color='#9b59b6', linewidth=1.5, alpha=0.8) 
 
        # Detectar picos en FFT con menor prominencia para capturar actividad anormal 
        peaks, _ = find_peaks(Pxx, prominence=fft_prominence*0.7) 
 
        # Mostrar picos en banda de interés (0-20 Hz para hipsarritmia) 
        mask = (f[peaks] <= 20) & (f[peaks] >= 0.5) 
        peaks = peaks[mask] 
 
        ax.plot(f[peaks], Pxx[peaks], "o", color='#e74c3c', markersize=8, 
                label=f'Picos ({len(peaks)})') 
 
        # Anotar frecuencias patológicas 
            # Note: Using len(peaks) > 0 to prevent errors if no peaks are found
        if len(peaks) > 0:
            # We need to ensure we don't try to access more than the number of peaks available
            for j, p in enumerate(peaks): 
                if j < 5:  # Mostrar hasta 5 frecuencias relevantes 
                    ax.annotate(f'{f[p]:.1f}Hz\n{Pxx[p]:.1f}', 
                                (f[p], Pxx[p]), 
                                textcoords="offset points", xytext=(0,10), 
                                ha='center', fontsize=9, 
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.set_xlim(0, 40) 
        ax.set_title('Espectro de Potencia - Hipsarritmia', fontsize=14) 
        ax.set_xlabel('Frecuencia (Hz)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        plt.tight_layout() 
        plt.show() 
 
# 6. Función principal 
def main(): 
    print("Iniciando análisis EEG...") 
 
    # Descargar datos si es necesario 
    descargar_datos() 
 
    # Generar datos simulados 
    print("Generando EEG normal simulado...") 
    eeg_sano = np.array([generar_eeg_sano(DURACION) for _ in CANALES]) 
 
    # Cargar datos reales 
    print("Cargando datos del paciente...") 
    try: 
        eeg_paciente = cargar_datos_paciente() 
    except Exception as e: 
        # Mensaje si falla la lectura (generalmente porque el archivo no existe o está corrupto)
        print(f"No se pudieron cargar los datos del paciente: {e}") 
        print("¡El archivo 'data/chb21_01.edf' fue eliminado y se intentará descargar de nuevo en la próxima ejecución!")
        return # Si falla la carga, detenemos el programa.
 
    # Visualizar comparación 
    print("Generando visualización...") 
    visualizar_comparacion(eeg_sano, eeg_paciente) 
    print("Análisis completado.") 
    
if __name__ == "__main__": 
    main()