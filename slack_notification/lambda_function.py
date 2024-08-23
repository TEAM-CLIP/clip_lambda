import json
import os

import requests
import mysql.connector
import boto3


def get_secret(secret_id):
    region_name = "ap-northeast-2"
    session = boto3.session.Session()
    secret_manager_client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    secret_value = secret_manager_client.get_secret_value(SecretId=secret_id)

    return json.loads(secret_value['SecretString'])


def get_mysql_connection(properties):
    conn = mysql.connector.connect(
        host=properties['DB_HOST'],
        user=properties['DB_USERNAME'],
        password=properties['DB_PASSWORD'],
        database=properties['DB_NAME']
    )

    return conn


def get_request_detail(record_id, cursor):
    select_query = "select * from recommend_request where id = %s"
    cursor.execute(select_query, (record_id,))
    result = cursor.fetchone()
    return result

def send_message(record_id, webhook_url):
    conn = get_mysql_connection(get_secret("chiksnap/db"))
    cursor = conn.cursor()

    print(f"record_id: {record_id}")

    request_detail = get_request_detail(record_id, cursor)
    print(f"request_detail: {request_detail}")
    phone_number = request_detail[1]
    prefer_style = request_detail[2]

    data = {
        'text': f"""
        새로운 추천 요청이 들어왔어요! 🎉
        - 전화번호: {phone_number}
        - 선호 스타일: {prefer_style}
        """.strip()
    }

    print(f"send data: {data}")

    requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

    cursor.close()
    conn.close()
    print("message sent successfully")



def handler(event, context):
    try:
        webhook_url = os.environ['RECOMMEND_SLACK_URL']

        meta_datas = event['Records']
        for meta_data in meta_datas:
            message = json.loads(meta_data['body'])
            data = message['body']
            record_id = data['record_id']
            send_message(record_id, webhook_url)

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': "error occurred while processing request"
        }

    return {
        'statusCode': 200,
        'body': 'processed successfully'
    }
