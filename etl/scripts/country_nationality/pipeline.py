"""This script cleans the country to nationality csv. Meant to be ran only once"""

import os
import pandas as pd

from lib.etl import extract, load

script_path = os.path.dirname(__file__)


def transform(df: pd.DataFrame) -> str:
    output_path = f"{script_path}/transformed.parquet"
    print(f"[INFO] Transforming dataframe and storing csv to {output_path}")

    # Groups by nationality and combines country names into a list, named "Countries"
    aggregated = df.groupby("Nationality").agg(Countries=("Name", list)).reset_index()

    aggregated.to_parquet(
        output_path, engine="pyarrow"
    )  # pandas handles schema using the dataframe types
    print(f"Parquet file saved to {output_path}")

    return output_path


def pipeline():
    raw_path = f"{script_path}/raw.csv"

    ###
    # Extract df from CSV
    ##
    df = extract(raw_path)

    ###
    # Load raw CSV to raw bucket for BQ raw table
    ###
    load(
        source_path=raw_path,
        bucket="f1_wc_data_raw",
        prefix="country_nationality",
        dest_name="data.csv",
    )

    ###
    # Transform and Aggregate to a Parquet file
    ###
    output_path = transform(df)

    ###
    # Load Parquet file to curated bucket
    ###
    load(
        source_path=output_path,
        bucket="f1_wc_data_curated",
        prefix="country_nationality",
        dest_name="data.parquet",
    )

    print(f"[INFO] Done extracting, transforming, and loading country nationality csv")


if __name__ == "__main__":
    pipeline()
