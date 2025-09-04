from __future__ import annotations

import pendulum
from airflow.decorators import dag, task
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset

@dag(
    dag_id="daily_data_ingestion_and_validation",
    schedule="@daily",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["data-pipeline", "etl"],
)
def data_ingestion_dag():
    @task
    def extract_data_from_source() -> str:
        # Logika untuk mengekstrak data (misalnya, dari API atau dump DB)
        # dan menyimpannya ke file CSV sementara.
        # Mengembalikan path ke file CSV.
        print("Mengekstrak data...")
        # Placeholder: ganti dengan logika ekstraksi nyata
        return "/tmp/raw_data.csv"

    @task
    def validate_data_with_great_expectations(csv_path: str) -> bool:
        # Memuat data dan mendefinisikan ekspektasi
        import pandas as pd
        df = pd.read_csv(csv_path)
        dataset = PandasDataset(df)
        
        # Contoh ekspektasi
        dataset.expect_column_to_not_be_null("user_id")
        dataset.expect_column_values_to_be_in_set("event_type", ["view", "purchase"])
        
        validation_result = dataset.validate()
        if not validation_result["success"]:
            raise ValueError("Validasi data gagal!", validation_result)
        print("Validasi data berhasil.")
        return True

    @task
    def load_data_to_datalake(csv_path: str, validation_status: bool):
        if not validation_status:
            print("Melewatkan pemuatan data karena validasi gagal.")
            return

        # Logika untuk memuat data dari CSV ke data lake (MinIO)
        # sebagai file Parquet.
        import pandas as pd
        df = pd.read_csv(csv_path)
        # Placeholder: ganti dengan koneksi MinIO nyata
        df.to_parquet("s3://bronze/events/daily_events.parquet")
        print("Data berhasil dimuat ke data lake.")

    raw_data_path = extract_data_from_source()
    is_valid = validate_data_with_great_expectations(raw_data_path)
    load_data_to_datalake(raw_data_path, is_valid)

data_ingestion_dag()