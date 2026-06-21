from pathlib import Path

from google.cloud import storage

from src.config.settings import BUCKET_NAME

FILES_TO_UPLOAD = {
    "data/bronze/german.data": "bronze/german.data",
    "data/silver/german_credit_silver.parquet": "silver/german_credit_silver.parquet",
    "data/gold/credit_risk_summary.parquet": "gold/credit_risk_summary.parquet",
    "data/gold/purpose_risk_summary.parquet": "gold/purpose_risk_summary.parquet",
    "data/gold/age_risk_summary.parquet": "gold/age_risk_summary.parquet",
}

def upload_file_to_gcs(local_path: str, destination_blob_name: str) -> None:
    # Upload a local file to Google Cloud Storage
    file_path = Path(local_path)

    if not file_path.exists():
        print(f"Arquivo não encontrado, ignorando: {local_path}")
        return

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(local_path)

    print(f"Arquivo enviado para GCS: gs://{BUCKET_NAME}/{destination_blob_name}")


def upload_to_gcs() -> None:
    # Upload Bronze, Silver and Gold outputs to Google Cloud Storage
    for local_path, destination_blob_name in FILES_TO_UPLOAD.items():
        upload_file_to_gcs(local_path, destination_blob_name)


if __name__ == "__main__":
    upload_to_gcs()