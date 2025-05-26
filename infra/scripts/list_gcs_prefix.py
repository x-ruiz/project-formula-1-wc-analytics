import os
import json

from google.cloud import storage


def list_gcs_prefixes(bucket: str, prefix: str) -> list[str]:
    """
    This function gets all the top level prefixes from a
    given GCS bucket assuming a delimiter of /

    It prints out a json to stdout for terraform to use. This
    script should ONLY print the json dump to stdout, no other
    logs or debug statements.

    Parameters:
    bucket (str): name of bucket to get prefixes from
    prefix (str): parent prefix to scope down search for
    """
    project_name = "formula-1-wc-analytics"
    output = []

    # print(f"[INFO] Listing gcs prefixes for bucket {bucket} under prefix {prefix}")
    client = storage.Client(project=project_name)

    objects = client.list_blobs(bucket, prefix=prefix)
    for obj in objects:
        # get the prefix after root level raw dir, assumes raw is parent
        raw_prefix = obj.name.split("/")[1]
        # print(raw_prefix)
        output.append(raw_prefix)

    return output


if __name__ == "__main__":
    import sys

    input_data = json.load(sys.stdin)  # get inputs from tf module
    bucket_name = input_data.get("bucket_name")
    prefix = input_data.get("prefix")
    output_result = {"all_prefixes_json": "", "prefix_count": "", "source_bucket": ""}

    if not bucket_name:
        sys.stderr.write("Bucket name not provided")
        sys.exit(1)

    try:
        prefixes = list_gcs_prefixes(bucket=bucket_name, prefix=prefix)
        output_result["all_prefixes_json"] = json.dumps(
            prefixes
        )  # List as a JSON string
        output_result["prefix_count"] = str(len(prefixes))  # Count as a string
        output_result["source_bucket"] = bucket_name  # Confirm the input bucket

        print(json.dumps(output_result))
    except Exception as e:
        print(json.dumps(output_result))
        sys.stderr.write(f"Error getting gcs prefixes: {e} \n")
        # sys.exit(1)
    # print(list_gcs_prefixes("f1_wc_1950_2020", "raw"))
