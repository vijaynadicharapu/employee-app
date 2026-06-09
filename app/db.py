import os
import json
import boto3
import psycopg2

SECRET_NAME = os.getenv("SECRET_NAME", "rdsaccess")
REGION = os.getenv("REGION", "us-east-1")

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
        database=creds.get("dbname", "postgres"),
        user=creds["username"],
        password=creds["password"],
        port=creds.get("port", 5432)
    )
