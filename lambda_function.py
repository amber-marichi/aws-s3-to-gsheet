import boto3
import csv
import gspread


bucket_name = ""
s3file_name = ""
gsheet_name = ""


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=s3file_name)
    
    file_data = s3_response["Body"].read().decode("UTF-8").splitlines()
    csv_data = csv.reader(file_data)

    write_sheet(csv_data)


def write_sheet(name_age_list):
    gc = gspread.service_account(filename="google_service_account_creds.json")
    gsheet = gc.open(gsheet_name)

    for i, row in enumerate(name_age_list):
        if i == 0:
            continue
        gsheet.sheet1.append_row(row, table_range="A2")
