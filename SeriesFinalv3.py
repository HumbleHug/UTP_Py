import os
import requests
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.signal import welch, find_peaks
import pyedflib

# 1. Configuración
PACIENTES = {
    "chb01": ["T8-P8", "T7-FT9"],
    "chb02": ["C3-P3", "T8-P8"]
}

FS = 256
DURACION = 2
URL_BASE = "https://physionet.org/files/chbmit/1.0.0/"

# 2. Descargar archivo EDF
def descargar_datos(paciente):
    os.makedirs("data", exist_ok=True)
    archivo_edf = f"{paciente}_01.edf"
    ruta_archivo = f"data/{archivo_edf}"

    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)

    print(f"\nDescargando archivo {archivo_edf} ...")
    url = f"{URL_BASE}{paciente}/{archivo_edf}"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(ruta_archivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Descarga completada. Archivo guardado en {ruta_archivo}")
    except Exception as e:
        print(f"Error al descargar: {e}")
        raise

# 3. EEG normal simulado
def generar_eeg_sano(duracion):
    t = np.arange(0, duracion, 1/FS)
    alpha = 40*np.sin(2*np.pi*10*t)
    beta  = 20*np.sin(2*np.pi*20*t)
    theta = 15*np.sin(2*np.pi*5*t)
    ruido = np.random.normal(0, 8, len(t))
    return alpha + beta + theta + ruido

# 4. Cargar datos EDF reales
def cargar_datos_paciente(paciente, canales):
    archivo = f"data/{paciente}_01.edf"
    with pyedflib.EdfReader(archivo) as f:
        labels = f.getSignalLabels()
        print("Canales disponibles:", labels)

        indices = [labels.index(c) for c in canales]
        señales = [f.readSignal(i)[:FS*DURACION] for i in indices]

    return np.array(señales)

# 5. Visualización + picos + FFT + PDF
def visualizar_comparacion(sano, paciente_data, paciente, canales):
    t = np.arange(0, DURACION, 1/FS)

    plt.style.use('seaborn-v0_8')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

    for i, canal in enumerate(canales):
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f"Análisis EEG – Paciente {paciente}, Canal {canal}", fontsize=16)

        eeg_prom = 15
        fft_prom = 2

        # --- 1. EEG SANO ---
        ax = axs[0, 0]
        ax.plot(t, sano[i], '#3498db', linewidth=1.5)
        peaks, _ = find_peaks(sano[i], prominence=eeg_prom)
        ax.plot(t[peaks], sano[i][peaks], "o", color='red')
        ax.set_title("EEG Normal Simulado")

        # --- 2. EEG PACIENTE ---
        ax = axs[0, 1]
        ax.plot(t, paciente_data[i], '#9b59b6', linewidth=1.5)
        peaks, _ = find_peaks(paciente_data[i], prominence=eeg_prom, distance=int(FS*0.05))
        ax.plot(t[peaks], paciente_data[i][peaks], "o", color='red')
        ax.set_title("EEG Paciente")

        # --- 3. FFT SANO ---
        ax = axs[1, 0]
        f, Pxx = welch(sano[i], FS, nperseg=1024)
        ax.plot(f, Pxx)
        peaks, _ = find_peaks(Pxx, prominence=fft_prom)
        mask = f[peaks] <= 40
        peaks = peaks[mask]
        ax.plot(f[peaks], Pxx[peaks], "o", color='red')
        ax.set_xlim(0, 40)
        ax.set_title("FFT Normal")

        # --- 4. FFT PACIENTE ---
        ax = axs[1, 1]
        f, Pxx = welch(paciente_data[i], FS, nperseg=1024)
        ax.plot(f, Pxx)
        peaks, _ = find_peaks(Pxx, prominence=fft_prom*0.7)
        mask = (f[peaks] <= 20) & (f[peaks] >= 0.5)
        peaks = peaks[mask]
        ax.plot(f[peaks], Pxx[peaks], "o", color='red')
        ax.set_xlim(0, 40)
        ax.set_title("FFT Paciente")

        plt.tight_layout()

        # ---- Guardar PDF ANTES del show ----
        os.makedirs("pdf", exist_ok=True)
        nombre_pdf = f"pdf/{paciente}_{canal}.pdf"
        plt.savefig(nombre_pdf)
        print(f"PDF guardado: {nombre_pdf}")

        plt.show()

# 6. MAIN
def main():
    print("\n=== INICIANDO ANÁLISIS EEG ===")

    for paciente, canales in PACIENTES.items():
        print(f"\n-----------------------------")
        print(f" Analizando {paciente}")
        print(f"-----------------------------")

        descargar_datos(paciente)

        eeg_sano = np.array([generar_eeg_sano(DURACION) for _ in canales])
        eeg_paciente = cargar_datos_paciente(paciente, canales)

        visualizar_comparacion(eeg_sano, eeg_paciente, paciente, canales)

    print("\n=== ANÁLISIS COMPLETADO ===")

if __name__ == "__main__":
    main()
