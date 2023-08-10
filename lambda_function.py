import boto3
import csv
import gspread
import os


def lambda_handler(event, context):
    my_session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY"),
    )

    csv_data = read_file_from_s3(my_session)
    write_sheet(csv_data)


def read_file_from_s3(session):
    s3_client = session.client("s3")
    s3_response = s3_client.get_object(
        Bucket=os.environ.get("BUCKET_NAME"),
        Key=os.environ.get("FILE_NAME")
    )
    
    file_data = s3_response["Body"].read().decode("UTF-8").splitlines()
    return csv.reader(file_data)


def write_sheet(name_age_list):
    gc = gspread.service_account(filename="google_service_account_creds.json")
    gsheet = gc.open(os.environ.get("SHEET_NAME"))

    for i, row in enumerate(name_age_list):
        if i == 0:
            continue
        gsheet.sheet1.append_row(row, table_range="A2")
