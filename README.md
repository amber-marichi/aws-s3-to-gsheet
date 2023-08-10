## aws-s3-to-gsheet
AWS Lambda raw script to transfer data from .csv file in S3 bucket to google spreadsheet.

### Configuration

#### Google sheet

1. [Google Developer Console](https://console.developers.google.com/)

2. Create a Project and Enable Google Sheet API and Google Drive API

3. Create service account

4. Download JSON file with service account credentials into `google_service_account_creds.json`

5. Create Google Sheet, add service account mail via 'Share' button



#### To test locally with docker

6. Build your image from Dockerfile
```sh
docker build -t docker-image .
```

7. Set necessary variables in .env file:
```sh
BUCKET_NAME=
FILE_NAME=
SHEET_NAME=
AWS_KEY_ID=
AWS_ACCESS_KEY=
```

8. Run docker container with variables from .env file:
```sh
docker run -p 9000:8080 --env-file .env docker-image
```

9. Now to test invoke lambda from outside:
```sh
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```
