import os

import pandas as pd
import kagglehub

from pendulum import datetime
from airflow.decorators import dag, task
from kagglehub import KaggleDatasetAdapter
from google.cloud import storage


@dag(start_date=datetime(2025, 1, 1), schedule="@once")
def raw_data_etl():
    """
    Executes an ETL (Extract, Transform, Load) pipeline for raw Formula 1 data.

    This function orchestrates the following steps:
    1. Extracts data from a Kaggle csv.
    2. Transforms the extracted data into a Parquet file format.
    3. Loads the transformed data into a Google Cloud Storage (GCS) bucket.

    Tasks:
        - extract_from_kaggle: Downloads the specified csv from Kaggle and loads it into a pandas DataFrame.
        - transform_to_parquet: Converts the DataFrame into a Parquet file and saves it locally.
        - load_to_gcs: Uploads the Parquet file to a specified GCS bucket.

    Variables:
        data (str): The name of the dataset to process (e.g., "circuits").
        gcp_project (str): The Google Cloud project ID.
        raw_bucket (str): The name of the GCS bucket where the data will be stored.

    Returns:
        None
    """
    data = "circuits"
    gcp_project = "formula-1-wc-analytics"
    raw_bucket = "f1_wc_1950_2020_raw"

    @task()
    def extract_from_kaggle() -> pd.DataFrame:
        print(f"Extracting ---{data}--- from skaggle")
        # Download latest version
        df = kagglehub.load_dataset(
            handle="rohanrao/formula-1-world-championship-1950-2020",
            adapter=KaggleDatasetAdapter.PANDAS,
            path=f"{data}.csv",
        )

        print("Extracted df", df.head())
        return df

    @task()
    def transform_to_parquet(raw_df: pd.DataFrame) -> str:
        parquet_path = os.path.join(
            "/tmp", f"{data}_df.parquet"
        )  # Using os.path.join to be compatible on different systems
        print(f"Transforming ---{data}--- to parquet file")
        raw_df.to_parquet(
            parquet_path, engine="pyarrow"
        )  # pandas handles schema using the dataframe types

        print(f"Parquet file saved to {parquet_path}")
        return str(parquet_path)

    @task()
    def load_to_gcs(parquet_path: str) -> bool:
        # lifecycle rule set up to clear files under test every day
        destination_path = f"test/{data}.parquet"
        client = storage.Client(project=gcp_project)
        bucket = client.bucket(raw_bucket)
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(parquet_path)

        return True

    # Dependency Graph
    raw_df = extract_from_kaggle()
    parquet_file_path = transform_to_parquet(raw_df)
    load_to_gcs(parquet_file_path)


raw_data_etl()
