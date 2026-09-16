import boto3
import csv
import io
import urllib.parse

s3 = boto3.client("s3")


def lambda_handler(event, context):

    print("Supplier ingestion Lambda started")

    # Get bucket and file name from the S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"]
    )

    print(f"Processing file: s3://{bucket}/{key}")

    # Read the file from S3
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    content = response["Body"].read().decode("utf-8")

    # Parse CSV
    reader = csv.DictReader(
        io.StringIO(content)
    )

    orders = list(reader)

    print(f"Successfully processed {len(orders)} orders")

    for order in orders:
        print(order)

    return {
        "statusCode": 200,
        "recordsProcessed": len(orders)
    }