import boto3
import csv
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


def lambda_handler(event, context):
    csv_data = read_file_from_s3()
    write_sheet(csv_data)


def read_file_from_s3():
    s3_client = boto3.client("s3")
    s3_response = s3_client.get_object(
        Bucket=os.environ.get("BUCKET_NAME"),
        Key=os.environ.get("FILE_NAME")
    )

    file_data = s3_response["Body"].read().decode("UTF-8").splitlines()
    return csv.reader(file_data)


def get_gsheet():
    credentials = service_account.Credentials.from_service_account_file(
        "google_service_account_creds.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=credentials)


def write_sheet(name_age_list):
    gsheet = get_gsheet()
    rows = {
        'values' : list(name_age_list)[1:]
    }

    resp = gsheet.spreadsheets().values().append(
        spreadsheetId=os.environ.get("SPREADSHEET_ID"),
        range="A1",
        valueInputOption="RAW",
        body=rows).execute()

    print(f"{resp['updates']['updatedRows']} new rows added.")
