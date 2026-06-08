import json
import boto3
import psycopg2

SECRET_NAME="employee-db-secret"
REGION="us-east-1"

def get_connection():

    client = boto3.client(
        "secretsmanager",
        region_name=REGION
    )

    secret = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    creds = json.loads(secret["SecretString"])

    return psycopg2.connect(
        host=creds["host"],
        database=creds["dbname"],
        user=creds["username"],
        password=creds["password"],
        port=5432
    )