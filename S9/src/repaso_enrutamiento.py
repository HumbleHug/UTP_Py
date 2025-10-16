from pathlib import Path

#enrutamiento
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR  = ROOT / "S9" / "data" / "raw"   #Ingresa a raw
FILENAME= "voltaje_sensor_10000.csv"     #Ingresa al archivo
CSV_PATH = DATA_DIR / FILENAME      # Combina la carpeta y el nombre del archivo

if not CSV_PATH.exists():
    raise FileNotFoundError(f"No existe: {CSV_PATH}")
OUT_DIR = ROOT/CSV_PATH.stem    
OUT_DIR.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe

nuevo = f"{CSV_PATH.stem.replace('clean','limpios')}"   # Reemplaza 'clean' por 'limpios'
prefijo, estado, n = CSV_PATH.stem.split("_")   # Divide el nombre en tres partes separadas por "_"
nuevo2 = f"{prefijo}_sensorn_{n}{CSV_PATH.suffix}"  # Crea un nuevo nombre agregando 'sensorn' antes del número

#comando glob
archivos = DATA_DIR.glob("*.csv")   # Busca todos los archivos .csv dentro de data/raw

In_file, Out = [],[]
for p in archivos:                                  # Recorre cada archivo encontrado
    prefijo, estado, n = p.stem.split("_")          # Divide el nombre del archivo actual en tres partes
    nuevo2 = f"{prefijo}_sensorn_{n}{p.suffix}"     # Crea un nuevo nombre con el mismo formato
    In_file.append(p.stem)                          # Agrega el nombre original (sin extensión) a la lista In_file
    Out.append(nuevo2)                              # Agrega el nuevo nombre generado a la lista Out
