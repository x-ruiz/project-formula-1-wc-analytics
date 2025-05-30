"""Airflow ETL to extract CSVs for Formula 1 Kaggle Dataset"""

import os

import pandas as pd
import kagglehub
import kaggle
import pendulum

# from pendulum import datetime
from airflow.decorators import dag, task

# from kagglehub import KaggleDatasetAdapter
from google.cloud import storage


@dag(start_date=pendulum.datetime(2025, 1, 1), schedule="@once")
def ingestion_etl():
    """
    Executes an EL (Extract, Load) ingestion pipeline for raw Formula 1 data.

    This function orchestrates the following steps:
    1. Extracts data from a Kaggle csv.
    2. Transforms to parquet
    3. Loads the transformed data into a Google Cloud Storage (GCS) bucket.

    Tasks:
        - extract_from_kaggle: Downloads the specified csv from Kaggle and
          loads it into a pandas DataFrame before saving to a CSV.
        - transform_to_parquet: Transforms DataFrame to parquet file
        - load_to_gcs: Uploads the CSV file to a specified GCS bucket.

    Variables:
        gcp_project (str): The Google Cloud project ID.
        raw_bucket (str): The name of the GCS bucket where the data will be stored.
        dataset (str): The name of the Kaggle dataset to pull files from.

    Returns:
        None
    """
    gcp_project = "formula-1-wc-analytics"
    raw_bucket = "f1_wc_data_raw"
    dataset = "rohanrao/formula-1-world-championship-1950-2020"
    current_date = pendulum.now("America/Chicago").date()

    @task()
    def list_files() -> list[str]:
        output = []
        files = kaggle.api.dataset_list_files(dataset).files

        for f in files:
            # remove .csv extension
            filename = f.name.split(".")[0]
            output.append(filename)

        print(f"Files to be processed: {output}")
        return output

    @task(map_index_template="{{ name }}")
    def get_name(name: str) -> str:
        print(f"Running ETL pipeline for ----{name}----")
        return name

    @task(map_index_template="{{ name }}")
    def extract_from_kaggle(name: str) -> pd.DataFrame:
        print(f"Extracting ---{name}--- from skaggle")
        output_path = os.path.join("/tmp", f"{name}_raw.csv")
        # Download latest version
        df = kagglehub.load_dataset(
            handle=dataset,
            adapter=kagglehub.KaggleDatasetAdapter.PANDAS,
            path=f"{name}.csv",
        )
        print("Extracted df", df.head())
        df.to_csv(output_path)

        # Couple the results with name for transform step
        return {"raw_df": df, "name": name}

    @task(map_index_template="{{ name }}")
    def transform_to_parquet(raw_df: pd.DataFrame, name: str) -> str:
        parquet_path = os.path.join(
            "/tmp", f"{name}_df.parquet"
        )  # Using os.path.join to be compatible on different systems
        print(f"Transforming ---{name}--- to parquet file")
        raw_df.to_parquet(
            parquet_path, engine="pyarrow"
        )  # pandas handles schema using the dataframe types
        print(f"Parquet file saved to {parquet_path}")

        # Couple the results with name for load step
        return {"parquet_path": str(parquet_path), "name": name}

    @task(map_index_template="{{ name }}")
    def load_to_gcs(parquet_path: str, name: str) -> bool:
        # lifecycle rule set up to clear files under test every day
        destination_path = f"1950_2020/{name}/dt={current_date}/data.parquet"
        client = storage.Client(project=gcp_project)
        bucket = client.bucket(raw_bucket)
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(parquet_path)

        return True

    # Dependency Graph
    files = list_files()
    names_expanded = get_name.expand(name=files)
    raw_df_expanded = extract_from_kaggle.expand(name=names_expanded)
    parquet_file_expanded = transform_to_parquet.expand_kwargs(raw_df_expanded)
    load_to_gcs.expand_kwargs(parquet_file_expanded)


ingestion_etl()
