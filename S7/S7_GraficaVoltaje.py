import csv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#enrutamiento
ROOT=Path(__file__).resolve().parents[1]
DATA_DIR  = ROOT /"S4" / "processing"   #Ingresa a la semana 4
FILENAME= "voltajes_250_limpio.csv"     #Ingresa al archivo
Umbral_V=5.05
#carpeta de salidas
PLOTS_DIR = ROOT / "S7"/ "plots"    #Me deja el archivo en plots
#si no existe debe crearse
PLOTS_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = DATA_DIR / FILENAME
if not CSV_PATH.exists():
    raise FileNotFoundError(f"No existe: {CSV_PATH}")

#utilidades (especie de filtro)
#detecta que esta limitando al CSV
def detectar_delimitador(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        head = f.readline()
    return ";" if head.count(";") > head.count(",") else ","
#poner todos los tiempos a un mismo tipo
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

#crear las listas Tiempo,Voltajes,Control
Tiempo,Voltaje,Control=[],[],[]
delim = detectar_delimitador(CSV_PATH)
with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
    r=csv.DictReader(f,delimiter=delim)
    for row in r:
        t = parse_ts(row.get("Tiempo"))
        if t is None:
            continue
        
        v_raw = row.get("Voltaje") or row.get("value")
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

# ====== Gráfico 1: Línea Voltaje vs Tiempo + umbral + puntos alerta ======
alerta_t=[t for t, lab in zip(Tiempo,Control) if lab == "ALERTA"]
alerts_v = [v for v, lab in zip(Voltaje,Control) if lab == "ALERTA"]
plt.figure(figsize=(9, 4))
plt.plot(Tiempo, Voltaje, label="Voltaje (V)")
plt.scatter(alerta_t, alerts_v,color="#f40404d2",label=f"Alertas (> {Umbral_V} V)") #los puntos que sobresalen de 5V
plt.axhline(Umbral_V,color="#ff8400d2", linestyle=":", label=f"Umbral {Umbral_V} V")

ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.title(f"Voltaje vs Tiempo — {CSV_PATH.name}")
plt.xlabel("Tiempo"); plt.ylabel("V")
plt.grid(True); plt.legend()
plt.tight_layout()
out1 = PLOTS_DIR / f"volt_line_{CSV_PATH.stem}.pdf"
plt.savefig(out1, dpi=150); plt.show()
print("Guardado:", out1)

# ====== Gráfico 2: Histograma de Voltaje ======
plt.figure(figsize=(6, 4))
plt.hist(Voltaje, bins=20)
plt.title(f"Histograma de Voltaje — {CSV_PATH.name}")
plt.xlabel("V"); plt.ylabel("Frecuencia")
plt.grid(True)
plt.tight_layout()
out2 = PLOTS_DIR / f"volt_hist_{CSV_PATH.stem}.png"
plt.savefig(out2, dpi=150); plt.show()
print("Guardado:", out2)

# ====== Gráfico 3: Boxplot de Voltaje ======
plt.figure(figsize=(4, 5))
plt.boxplot(Voltaje, vert=True, showmeans=True)
plt.title(f"Boxplot de Voltaje — {CSV_PATH.name}")
plt.ylabel("V")
plt.grid(True)
plt.tight_layout()
out3 = PLOTS_DIR / f"volt_box_{CSV_PATH.stem}.png"
plt.savefig(out3, dpi=150); plt.show()
print("Guardado:", out3)