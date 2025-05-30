"""
This script will handle all ETL general methods.
Utilizes application credentials to run locally
"""

import argparse
import os

from google.cloud import storage
import pandas as pd

raw_data_abs_path = os.path.dirname(os.path.dirname(__file__))


def extract(file_path: str) -> pd.DataFrame:
    print(f"[INFO] Extracting file to dataframe {file_path}")
    df = pd.read_csv(file_path)
    return df


def load(source_path: str, bucket: str, prefix: str, dest_name: str):
    print(
        f"[INFO] Uploading file {source_path} to bucket {bucket} with path {prefix}/{dest_name}"
    )
    client = storage.Client(project="formula-1-wc-analytics")
    bucket = client.bucket(bucket)
    blob = bucket.blob(f"{prefix}/{dest_name}")

    # not including match generation since we are the only
    # ones uploading a file, no need to worry about
    # race conditions
    blob.upload_from_filename(source_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="GCSFileUploader",
        description="Script to upload any file to any bucket with any prefix",
    )
    parser.add_argument(
        "-s",
        "--source_path",
        required=True,
        help="Path of file to upload in relation to raw_data dir",
    )
    parser.add_argument(
        "-b",
        "--bucket",
        required=True,
        help="Full bucket name formatted starting after gs://",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        required=True,
        help="The full prefix in the bucket where the file will be stored",
    )
    parser.add_argument(
        "-d",
        "--dest_name",
        required=True,
        help="The file name to be saved in the bucket",
    )
    args = parser.parse_args()
    load(
        source_path=args.source_path,
        bucket=args.bucket,
        prefix=args.prefix,
        dest_name=args.dest_name,
    )
