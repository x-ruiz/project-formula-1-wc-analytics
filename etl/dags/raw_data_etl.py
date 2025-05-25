from pendulum import datetime

from airflow.decorators import dag, task
import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import os

@dag(
    start_date=datetime(2025, 1, 1),
    schedule="@once"
)
def raw_data_etl():
    data = "circuits"
    @task()
    def extract_from_kaggle() -> pd.DataFrame:
        print(f"Extracting ---{data}--- from skaggle")
        # Download latest version
        df = kagglehub.load_dataset(
            handle='rohanrao/formula-1-world-championship-1950-2020',
            adapter=KaggleDatasetAdapter.PANDAS,
            path=f"{data}.csv"
            )

        print("Extracted df", df.head())
        return df

    @task()
    def transform_to_parquet(raw_df: pd.DataFrame) -> str:
        parquet_path = os.path.join('/tmp', f'{data}_df.parquet') # Using os.path.join to be compatible on different systems
        print(f"Transforming ---{data}--- to parquet file")
        raw_df.to_parquet(parquet_path, engine='pyarrow') # pandas handles schema using the dataframe types

        print(f"Parquet file saved to {parquet_path}")
        return str(parquet_path)

    # Dependency Graph
    raw_df = extract_from_kaggle()
    transform_to_parquet(raw_df)



raw_data_etl()