from pathlib import Path

from google.cloud import bigquery

from src.config.settings import DATASET_ID, PROJECT_ID

TABLES_TO_LOAD = {
    "data/silver/german_credit_silver.parquet": "german_credit_silver",
    "data/gold/credit_risk_summary.parquet": "credit_risk_summary",
    "data/gold/purpose_risk_summary.parquet": "purpose_risk_summary",
    "data/gold/age_risk_summary.parquet": "age_risk_summary",
}

def load_parquet_to_bigquery(local_path: str, table_name: str) -> None:
    file_path = Path(local_path)

    if not file_path.exists():
        print(f"Arquivo não encontrado, ignorando: {local_path}")
        return

    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with file_path.open("rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            table_id,
            job_config=job_config,
        )

    job.result()

    table = client.get_table(table_id)
    print(f"Tabela carregada: {table_id} | Linhas: {table.num_rows}")


def load_to_bigquery() -> None:
    for local_path, table_name in TABLES_TO_LOAD.items():
        load_parquet_to_bigquery(local_path, table_name)


if __name__ == "__main__":
    load_to_bigquery()