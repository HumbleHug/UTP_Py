from pathlib import Path

#enrutamiento
ROOT=Path(__file__).resolve().parents[1]
DATA_DIR  = ROOT / "data" / "processed"   #Ingresa a processed
FILENAME= "voltajes_clean_01.csv"     #Ingresa al archivo
CSV_PATH = DATA_DIR / FILENAME

if not CSV_PATH.exists():
    raise FileNotFoundError(f"No existe: {CSV_PATH}")
OUT_DIR = ROOT/CSV_PATH.stem 
OUT_DIR.mkdir(parents=True, exist_ok=True)

nuevo = f"{CSV_PATH.stem.replace('clean','limpios')}"

prefijo, estado, n = CSV_PATH.stem.split("_")   # 'datos' , 'sucios' , '250'
nuevo2 = f"{prefijo}_sensorn_{n}{CSV_PATH.suffix}"
#comando glob
archivos = DATA_DIR.glob("*.csv")   #todos los .csv

In_file, Out = [],[]
for p in archivos:
    prefijo, estado, n = p.stem.split("_")
    nuevo2 = f"{prefijo}_sensorn_{n}{p.suffix}"
    In_file.append(p.stem)
    Out.append(p.stem)