import boto3
import csv
import json
from botocore.exceptions import ClientError

from google.oauth2 import service_account
from googleapiclient.discovery import build


def get_secret(secret_name):
    region_name = "eu-central-1"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as error:
        raise error

    # Decrypts secret using the associated KMS key.
    return json.loads(get_secret_value_response["SecretString"])


def lambda_handler(event, context):
    secrets = get_secret("vars-for-etl")

    csv_data = read_file_from_s3(
        secrets["bucket_name"],
        secrets["file_name"]
    )

    write_sheet(
        secrets["spreadsheet_id"],
        csv_data
    )


def read_file_from_s3(bucket_name, file_name):
    s3_client = boto3.client("s3")
    s3_response = s3_client.get_object(
        Bucket=bucket_name,
        Key=file_name
    )

    file_data = s3_response["Body"].read().decode("UTF-8").splitlines()
    return csv.reader(file_data)


def get_gsheet():
    credentials = service_account.Credentials.from_service_account_info(
        get_secret("google-service-acc-creds"),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=credentials)


def write_sheet(spreadsheet_id, name_age_list):
    gsheet = get_gsheet()
    rows = {
        "values" : list(name_age_list)[1:]
    }

    resp = gsheet.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="A1",
        valueInputOption="RAW",
        body=rows
    ).execute()

    print(f"{resp['updates']['updatedRows']} new rows added.")
