import os 
import requests 
import numpy as np 
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt 
from scipy.signal import welch, find_peaks 
import pyedflib 

# 1. Configuración 
FS = 256  # Frecuencia de muestreo 
DURACION = 2  # segundos 
URL_BASE = "https://physionet.org/files/chbmit/1.0.0/" 

# Lista de pacientes y sus canales específicos
PACIENTES_CONFIG = [
    {"id": "chb01", "canales": ["FP1-F7"]},
    {"id": "chb02", "canales": ["FP1-F7"]}
]

# 2. Descargar archivo EDF 
def descargar_datos(paciente_id): 
    os.makedirs("data", exist_ok=True) 
    archivo_edf = f"{paciente_id}_01.edf" 
    ruta_archivo = f"data/{archivo_edf}"
    
    if os.path.exists(ruta_archivo):
        pass 

    if not os.path.exists(ruta_archivo):
        print(f"[{paciente_id}] Descargando archivo {archivo_edf} desde {URL_BASE}{paciente_id}/...") 
        url = f"{URL_BASE}{paciente_id}/{archivo_edf}" 
        try: 
            response = requests.get(url, stream=True) 
            response.raise_for_status() 
            with open(ruta_archivo, 'wb') as f: 
                for chunk in response.iter_content(chunk_size=8192): 
                    f.write(chunk) 
            print(f"[{paciente_id}] Descarga completada.") 
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            raise
        except Exception as e: 
            print(f"Error general: {e}") 
            raise 
 
# 3. Generar EEG normal simulado 
def generar_eeg_sano(duracion): 
    t = np.arange(0, duracion, 1/FS) 
    alpha = 40 * np.sin(2 * np.pi * 10 * t) 
    beta = 20 * np.sin(2 * np.pi * 20 * t) 
    theta = 15 * np.sin(2 * np.pi * 5 * t) 
    ruido = np.random.normal(0, 1, len(t)) 
    return alpha + beta + theta + ruido 
 
# 4. Cargar datos reales del paciente 
def cargar_datos_paciente(paciente_id, canales_lista): 
    archivo_edf = f"data/{paciente_id}_01.edf" 
    try: 
        with pyedflib.EdfReader(archivo_edf) as f: 
            print(f"[{paciente_id}] Canales disponibles: {len(f.getSignalLabels())}") 
            indices = [f.getSignalLabels().index(c) for c in canales_lista] 
            señales = [f.readSignal(i)[:FS*DURACION] for i in indices] 
        return np.array(señales) 
    except Exception as e: 
        print(f"Error al leer archivo EDF de {paciente_id}: {e}") 
        raise
 
# 5. Visualización con detección de picos 
def visualizar_comparacion(sano, paciente_signal, canales_lista, nombre_paciente): 
    t = np.arange(0, DURACION, 1/FS) 
 
    plt.style.use('seaborn-v0_8') 
    plt.rcParams['figure.facecolor'] = 'white' 
    plt.rcParams['axes.grid'] = True 
    plt.rcParams['grid.alpha'] = 0.3 
 
    for i, canal in enumerate(canales_lista): 
        fig, axs = plt.subplots(2, 2, figsize=(16, 12)) 
        
        # Título general
        fig.suptitle(f'Paciente: {nombre_paciente} | Canal {canal}', fontsize=16, y=0.99) 
 
        # Parámetros 
        eeg_prominence = 15 
        fft_prominence = 2 
 
        # --- 1. EEG Normal --- 
        ax = axs[0, 0] 
        ax.plot(t, sano[i], color='#3498db', linewidth=1.5, alpha=0.8, label='Señal') 
        peaks, _ = find_peaks(sano[i], prominence=eeg_prominence) 
        ax.plot(t[peaks], sano[i][peaks], "o", color='#e74c3c', markersize=8, label=f'Picos ({len(peaks)})') 
 
        if len(peaks) > 0: 
            top_3 = peaks[np.argsort(sano[i][peaks])[-3:]] 
            for p in top_3: 
                ax.annotate(f'{sano[i][p]:.1f}μV\n{t[p]:.2f}s', 
                            (t[p], sano[i][p]), 
                            textcoords="offset points", xytext=(0,10), 
                            ha='center', fontsize=9, 
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.margins(y=0.1)
        ax.set_title('EEG Normal Simulado', fontsize=14, pad=10) 
        ax.set_xlabel('Tiempo (s)', fontsize=12) 
        ax.set_ylabel('Amplitud (μV)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        # --- 2. EEG Paciente --- 
        ax = axs[0, 1] 
        ax.plot(t, paciente_signal[i], color='#9b59b6', linewidth=1.5, alpha=0.8, label='Señal') 
        peaks, _ = find_peaks(paciente_signal[i], prominence=eeg_prominence, distance=int(FS*0.05)) 
        ax.plot(t[peaks], paciente_signal[i][peaks], "o", color='#e74c3c', markersize=8, label=f'Picos ({len(peaks)})') 
 
        if len(peaks) > 0: 
            top_5 = peaks[np.argsort(paciente_signal[i][peaks])[-5:]] 
            for p in top_5: 
                ax.annotate(f'{paciente_signal[i][p]:.1f}μV\n{t[p]:.2f}s', 
                            (t[p], paciente_signal[i][p]), 
                            textcoords="offset points", xytext=(0,10), 
                            ha='center', fontsize=9, 
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.margins(y=0.1)
        ax.set_title('EEG Paciente con Epilepsia Refractaria', fontsize=14, pad=10) 
        ax.set_xlabel('Tiempo (s)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        # --- 3. FFT Normal --- 
        ax = axs[1, 0] 
        f, Pxx = welch(sano[i], FS, nperseg=1024) 
        ax.plot(f, Pxx, color='#3498db', linewidth=1.5, alpha=0.8) 
        peaks, _ = find_peaks(Pxx, prominence=fft_prominence) 
        mask = f[peaks] <= 40 
        peaks = peaks[mask] 
        ax.plot(f[peaks], Pxx[peaks], "o", color='#e74c3c', markersize=8, label=f'Picos ({len(peaks)})') 
 
        for j, p in enumerate(peaks): 
            if j < 3: 
                ax.annotate(f'{f[p]:.1f}Hz\n{Pxx[p]:.1f}', 
                            (f[p], Pxx[p]), 
                            textcoords="offset points", xytext=(0,10), 
                            ha='center', fontsize=9, 
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.margins(y=0.1)
        ax.set_xlim(0, 40) 
        ax.set_title('Espectro de Potencia - Normal', fontsize=14, pad=10) 
        ax.set_xlabel('Frecuencia (Hz)', fontsize=12) 
        ax.set_ylabel('Densidad de Potencia (μV²/Hz)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        # --- 4. FFT Paciente --- 
        ax = axs[1, 1] 
        f, Pxx = welch(paciente_signal[i], FS, nperseg=1024) 
        ax.plot(f, Pxx, color='#9b59b6', linewidth=1.5, alpha=0.8) 
        peaks, _ = find_peaks(Pxx, prominence=fft_prominence*0.7) 
        mask = (f[peaks] <= 20) & (f[peaks] >= 0.5) 
        peaks = peaks[mask] 
        ax.plot(f[peaks], Pxx[peaks], "o", color='#e74c3c', markersize=8, label=f'Picos ({len(peaks)})') 
 
        if len(peaks) > 0:
            for j, p in enumerate(peaks): 
                if j < 5: 
                    ax.annotate(f'{f[p]:.1f}Hz\n{Pxx[p]:.1f}', 
                                (f[p], Pxx[p]), 
                                textcoords="offset points", xytext=(0,10), 
                                ha='center', fontsize=9, 
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none")) 
 
        ax.margins(y=0.1)
        ax.set_xlim(0, 40) 
        ax.set_title('Espectro de Potencia - Epilepsia Refractaria', fontsize=14, pad=10) 
        ax.set_xlabel('Frecuencia (Hz)', fontsize=12) 
        ax.legend(loc='upper right') 
 
        plt.tight_layout(rect=[0, 0.03, 1, 0.96], h_pad=4.0) 
        
        nombre_pdf = f"{nombre_paciente}_{canal}.pdf"
        plt.savefig(nombre_pdf)
        print(f"Grafico guardado como: {nombre_pdf}")
        
        plt.show() 
 
# 6. Función principal 
def main(): 
    print("Iniciando análisis EEG Multi-paciente...") 
    for config in PACIENTES_CONFIG:
        p_id = config["id"]
        p_canales = config["canales"]
        print(f"\n--- PROCESANDO PACIENTE: {p_id} ---")
        descargar_datos(p_id) 
        print("Generando EEG normal simulado...") 
        eeg_sano = np.array([generar_eeg_sano(DURACION) for _ in p_canales]) 
        print(f"Cargando datos del paciente {p_id}...") 
        try: 
            eeg_paciente = cargar_datos_paciente(p_id, p_canales) 
            print(f"Generando visualización para {p_id}...") 
            visualizar_comparacion(eeg_sano, eeg_paciente, p_canales, p_id) 
        except Exception as e: 
            print(f"Saltando análisis de {p_id} debido a error: {e}") 
            continue
    print("\nAnálisis completo de todos los pacientes.") 
    
if __name__ == "__main__": 
    main()