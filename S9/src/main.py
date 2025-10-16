import csv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#ENRUTAMIENTO
ROOT=Path(__file__).resolve().parents[1]    #ROOT = S9
DATA_DIR  = ROOT / "data" / "raw"   #Ingresa a raw 
#comando glob
archivos=DATA_DIR.glob("*.csv")

PLOTS_DIR=ROOT/"plots"  #Ingresa a plots
PLOTS_DIR.mkdir(parents=True, exist_ok=True) #crear la carpeta si no existe
Umbral_V=5.1

def detectar_delimitador(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        head = f.readline()
    return ";" if head.count(";") > head.count(",") else ","

#poner todos los tiempos a un mismo formato
def parse_ts(s: str):
    s = (s or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    if "T" in s and len(s) >= 19:
        try:
            return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
    return None

for p in archivos:
    FILENAME= p.name
    CSV_PATH = DATA_DIR / FILENAME
    Tiempo, Voltaje, Control=[],[],[]
    delim=detectar_delimitador(CSV_PATH)
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        r=csv.DictReader(f,delimiter=delim)
        for row in r:
            t = parse_ts(row.get("tiempo"))
            if t is None:
                continue
            v_raw=row.get('voltaje') or row.get("value")
            try:
                v = float(str(v_raw).replace(",", "."))
            except (TypeError, ValueError):
                continue
            lab = "ALERTA" if v > Umbral_V else "OK"
            
            Tiempo.append(t)
            Voltaje.append(v)
            Control.append(lab)
            
    if not Tiempo:
        raise RuntimeError("No se pudieron leer datos válidos (timestamp/voltaje).")
    print(f"Leído: {CSV_PATH.name} — filas válidas: {len(Tiempo)}")

    #Hacer los graficos.
    #////grafico del tipo lineal/////
    alerta_t=[t for t, lab in zip(Tiempo,Control) if lab=="ALERTA"] #separa los tiempos donde sale una alerta
    alerts_v=[v for v, lab in zip(Voltaje,Control) if lab=="ALERTA"] #separa los voltjaes donde sale una alerta
    plt.figure(figsize=(9, 4)) #tamano de la figura
    plt.plot(Tiempo,Voltaje,color="#0039acea", linestyle="-",label="Voltaje (V)")
    plt.scatter(alerta_t, alerts_v,color="#f40404d2",label=f"Alertas (> {Umbral_V} V)")
    ax = plt.gca()
    
    plt.axhline(Umbral_V,color="#fd9800d2", linestyle=":", label=f"Umbral {Umbral_V} V")
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    plt.title(f"Voltaje vs Tiempo — {CSV_PATH.stem}".upper(),fontdict={'fontweight': 'bold'})
    plt.xlabel("Tiempo"); plt.ylabel("V")
    plt.grid(True); plt.legend()
    plt.tight_layout()
    out1 = PLOTS_DIR / f"volt_line_{CSV_PATH.stem}.png"
    plt.savefig(out1, dpi=400)
    print("Guardado:", out1)

    #//////HISTOGRAMA///////
    plt.figure(figsize=(6, 4))
    plt.hist(Voltaje, bins=30,orientation="vertical")
    plt.title(f"Histograma de Voltaje — {CSV_PATH.name}".upper(),fontdict={'fontweight': 'bold'})
    plt.xlabel("V"); plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.tight_layout()
    out2 = PLOTS_DIR / f"volt_hist_{CSV_PATH.stem}.png"
    plt.savefig(out2, dpi=150)
    print("Guardado:", out2)