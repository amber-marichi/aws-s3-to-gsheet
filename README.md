## aws-s3-to-gsheet
AWS Lambda raw script to transfer data from .csv file in S3 bucket to google spreadsheet.

### Configuration

#### Google sheet

1. [Google Developer Console](https://console.developers.google.com/)

2. Create a Project and Enable Google Sheet API and Google Drive API

3. Create service account

4. Download JSON file with service account credentials into `google_service_account_creds.json`

5. Create Google Sheet, add service account mail via 'Share' button



#### AWS Lambda Function

6. [Create Lambda function](https://console.aws.amazon.com/lambda/home)

7. Create Python3 layer with 'gspread' library and add it to Lambda

8. Upload .py file to Lambda

9. Set necessary variables to execute:
```sh
bucket_name = "name-of-your-s3-bucket"
s3file_name = "name-of-csv-file-in-bucket"
gsheet_name = "name-of-google-spreadsheet"
```