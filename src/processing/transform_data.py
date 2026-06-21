from pathlib import Path

import pandas as pd

from src.processing.mappings import (
    COLUMN_NAMES,
    TARGET_MAPPING,
    CATEGORICAL_MAPPINGS,
)

BRONZE_PATH = Path("data/bronze/german.data")
SILVER_PATH = Path("data/silver/german_credit_silver.parquet")


def transform_data() -> None:
    # Transform Bronze German Credit data into Silver Parquet
    if not BRONZE_PATH.exists():
        raise FileNotFoundError(f"Arquivo Bronze não encontrado: {BRONZE_PATH}")

    SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
        BRONZE_PATH,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES,
    )

    for column, mapping in CATEGORICAL_MAPPINGS.items():
        if column in df.columns:
            df[column] = df[column].map(mapping)

    df["target_label"] = df["target"].map(TARGET_MAPPING)

    df.to_parquet(SILVER_PATH, index=False)

    print(f"Arquivo Silver gerado: {SILVER_PATH}")
    print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")


if __name__ == "__main__":
    transform_data()