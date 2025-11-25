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

FS = 256       # Frecuencia de muestreo
DURACION = 2    # segundos
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

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(ruta_archivo, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("Descarga completada.")


# 3. Generar EEG normal simulado 
def generar_eeg_sano(duracion):
    t = np.arange(0, duracion, 1/FS)
    # Componentes rítmicas 
    alpha = 40 * np.sin(2 * np.pi * 10 * t)
    beta  = 20 * np.sin(2 * np.pi * 20 * t)
    # Ruido fisiológico simulado 
    theta = 15 * np.sin(2 * np.pi * 5 * t)
    ruido = np.random.normal(0, 8, len(t))
    return alpha + beta + theta + ruido


# 4. Cargar datos reales del paciente 
def cargar_datos_paciente(paciente, canales):
    archivo_edf = f"data/{paciente}_01.edf"

    with pyedflib.EdfReader(archivo_edf) as f:
        labels = f.getSignalLabels()
        print(f"Canales disponibles: {labels}")

        indices = [labels.index(c) for c in canales]
        señales = [f.readSignal(i)[:FS*DURACION] for i in indices]

    return np.array(señales)


# 5. Visualización con detección de picos 
def visualizar_comparacion(sano, paciente_data, paciente, canales):
    t = np.arange(0, DURACION, 1/FS)

    for i, canal in enumerate(canales):
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))

        # TITULO CON PACIENTE + CANAL
        fig.suptitle(f'Paciente {paciente} – Canal {canal}', fontsize=16, y=1.02)

        eeg_prominence = 15
        fft_prominence = 2

        # --- 1. EEG Normal ---
        ax = axs[0, 0]
        ax.plot(t, sano[i], color='#3498db')

        peaks, _ = find_peaks(sano[i], prominence=eeg_prominence)
        ax.plot(t[peaks], sano[i][peaks], "o", color='red')

        ax.set_title('EEG Normal Simulado')

        # --- 2. EEG Paciente --- 
        ax = axs[0, 1]
        ax.plot(t, paciente_data[i], color='#9b59b6')

        peaks, _ = find_peaks(paciente_data[i], prominence=eeg_prominence)
        ax.plot(t[peaks], paciente_data[i][peaks], "o", color='red')

        ax.set_title('EEG Paciente')

        # --- 3. FFT Normal --- 
        ax = axs[1, 0]
        f, Pxx = welch(sano[i], FS, nperseg=1024)
        ax.plot(f, Pxx)
        ax.set_xlim(0, 40)
        ax.set_title('FFT Normal')

        # --- 4. FFT Paciente --- 
        ax = axs[1, 1]
        f, Pxx = welch(paciente_data[i], FS, nperseg=1024)
        ax.plot(f, Pxx)
        ax.set_xlim(0, 40)
        ax.set_title('FFT Paciente')

        plt.tight_layout()

        # --- 4. Guardar PDF --- 
        os.makedirs("pdf", exist_ok=True)
        nombre_pdf = f"pdf/{paciente}_{canal}.pdf"
        plt.savefig(nombre_pdf)

        print(f"PDF guardado: {nombre_pdf}")

        plt.show()


# 6. Función principal 
def main():
    print("\n=== INICIANDO ANÁLISIS EEG ===")

    for paciente, canales in PACIENTES.items():

        print(f"\n==============================")
        print(f" Analizando {paciente}")
        print(f"==============================")

        descargar_datos(paciente)

        eeg_sano = np.array([generar_eeg_sano(DURACION) for _ in canales])
        eeg_paciente = cargar_datos_paciente(paciente, canales)

        visualizar_comparacion(eeg_sano, eeg_paciente, paciente, canales)

    print("\n=== ANÁLISIS COMPLETADO ===")


if __name__ == "__main__":
    main()