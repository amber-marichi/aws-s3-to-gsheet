import boto3
import csv
import json
from botocore.exceptions import ClientError


def get_secret(secret_name):
    region_name = "eu-central-1"

    client = boto3.client(
        service_name="secretsmanager",
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as error:
        raise error

    return json.loads(get_secret_value_response["SecretString"])


def lambda_handler(event, context):
    print(event)
    username = json.loads(event["body"]).get("username")
    if not username:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid request: No username found")
        }

    result = search_user(username)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }


def search_user(username):
    result = []
    for ind, user in enumerate(get_users()):
        if username in user[0]:
            result.append([ind, *user])
    return result


def get_users():
    secrets = get_secret("vars-for-etl")

    s3_client = boto3.client("s3")
    s3_response = s3_client.get_object(
        Bucket=secrets["bucket_name"],
        Key=secrets["file_name"]
    )

    file_data = s3_response["Body"].read().decode("UTF-8").splitlines()
    return list(csv.reader(file_data))
