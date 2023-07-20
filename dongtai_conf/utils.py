import base64
import json
import os
import sys

import boto3
from botocore.exceptions import ClientError


def aws_get_secret(base_dir: str):
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("REGION_NAME")
    secret_name = os.getenv("SECRET_NAME")
    if not all(
        [
            aws_access_key_id,
            aws_secret_access_key,
            region_name,
            secret_name,
        ]
    ):
        sys.exit("environment not set")
    session = boto3.session.Session()
    client = session.client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        service_name="secretsmanager",
        region_name=region_name,
    )

    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    config = json.loads(get_secret_value_response["SecretString"])["iast-config"]
    raw = config.encode("raw_unicode_escape")

    with open(os.path.join(base_dir, "dongtai_conf/conf/config.ini"), "w") as fp:
        fp.write(base64.b64decode(raw).decode("utf-8"))


def get_config(base_dir: str, target_cloud: str):
    if target_cloud == "AWS":
        aws_get_secret(base_dir)
    else:
        print("use local file")
