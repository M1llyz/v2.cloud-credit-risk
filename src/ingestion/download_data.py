from pathlib import Path
from urllib.request import urlretrieve

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
BRONZE_PATH = Path("data/bronze/german.data")

def download_data() -> None:
    # Download raw German Credit dataset into the Bronze layer
    BRONZE_PATH.parent.mkdir(parents=True, exist_ok=True)

    if BRONZE_PATH.exists():
        print(f"Arquivo Bronze já existe: {BRONZE_PATH}")
        return

    urlretrieve(DATA_URL, BRONZE_PATH)
    print(f"Arquivo baixado para: {BRONZE_PATH}")

if __name__ == "__main__":
    download_data()