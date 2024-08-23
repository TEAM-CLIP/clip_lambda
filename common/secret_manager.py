import boto3
import json

def get_secret_properties(secret_id):
    region_name = "ap-northeast-2"
    session = boto3.session.Session()
    secret_manager_client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    secret_value = secret_manager_client.get_secret_value(SecretId=secret_id)

    return json.loads(secret_value['SecretString'])