from pathlib import Path

import pandas as pd

SILVER_PATH = Path("data/silver/german_credit_silver.parquet")
GOLD_DIR = Path("data/gold")

def generate_gold() -> None:
    # Generate analytical Gold datasets from Silver data
    if not SILVER_PATH.exists():
        raise FileNotFoundError(f"Arquivo Silver não encontrado: {SILVER_PATH}")

    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(SILVER_PATH)

    credit_risk_summary = (
        df.groupby("target_label")
        .agg(
            total_customers=("target_label", "count"),
            avg_credit_amount=("credit_amount", "mean"),
            avg_age=("age", "mean"),
            avg_duration_months=("duration_months", "mean"),
        )
        .reset_index()
    )

    purpose_risk_summary = (
        df.groupby(["purpose", "target_label"])
        .agg(
            total_customers=("target_label", "count"),
            avg_credit_amount=("credit_amount", "mean"),
        )
        .reset_index()
    )

    age_risk_summary = (
        df.assign(
            age_group=pd.cut(
                df["age"],
                bins=[0, 25, 35, 50, 120],
                labels=["18-25", "26-35", "36-50", "51+"],
            )
        )
        .groupby(["age_group", "target_label"], observed=False)
        .agg(
            total_customers=("target_label", "count"),
            avg_credit_amount=("credit_amount", "mean"),
        )
        .reset_index()
    )

    credit_risk_summary.to_parquet(GOLD_DIR / "credit_risk_summary.parquet", index=False)
    purpose_risk_summary.to_parquet(GOLD_DIR / "purpose_risk_summary.parquet", index=False)
    age_risk_summary.to_parquet(GOLD_DIR / "age_risk_summary.parquet", index=False)

    print("Arquivos Gold gerados em data/gold:")
    print("- credit_risk_summary.parquet")
    print("- purpose_risk_summary.parquet")
    print("- age_risk_summary.parquet")


if __name__ == "__main__":
    generate_gold()