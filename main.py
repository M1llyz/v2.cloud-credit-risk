from src.ingestion.download_data import download_data
from src.processing.transform_data import transform_data
from src.processing.generate_gold import generate_gold
from src.cloud.upload_to_gcs import upload_to_gcs
from src.cloud.load_to_bigquery import load_to_bigquery


def main() -> None:
    print("Iniciando pipeline de risco de crédito...")

    download_data()
    transform_data()
    generate_gold()
    upload_to_gcs()
    load_to_bigquery()

    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    main()