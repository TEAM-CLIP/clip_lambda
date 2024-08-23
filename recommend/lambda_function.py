import json
import os

import mysql.connector
import boto3

import common.secret_manager as secret_manager


def get_mysql_connection(properties):
    conn = mysql.connector.connect(
        host=properties['DB_HOST'],
        user=properties['DB_USERNAME'],
        password=properties['DB_PASSWORD'],
        database=properties['DB_NAME']
    )

    return conn


def initialize_table(cursor):
    table_create_if_not_exists_query = """
    create table if not exists recommend_request(
        id bigint primary key auto_increment,
        phone_number varchar(50) not null,
        prefer_style text not null,
        created_at datetime default current_timestamp
    );
    """

    cursor.execute(table_create_if_not_exists_query)


def add_recommend_request(cursor, message):
    initialize_table(cursor)
    insert_query = """
    insert into recommend_request(phone_number, prefer_style) values (%s, %s)
    """
    cursor.execute(insert_query, (message['phone_number'], message['prefer_style']))

    return cursor.lastrowid

def create_slack_message(record_id):
    message = {
        'message_type': "photographer_recommend",
        'body': {
            "record_id": record_id
        }
    }

    return json.dumps(message)

def send_queue(record_id):
    message = create_slack_message(record_id)
    sqs_client = boto3.client("sqs")

    sqs_client.send_message(QueueUrl = os.environ['SLACK_SQS_URL'], MessageBody = message)


def handler(event, context):
    try:
        request = json.dumps(event)

        # db_properties = get_secret("chiksnap/db")
        db_properties = secret_manager.get_secret_properties("chiksnap/db")

        conn = get_mysql_connection(db_properties)
        cursor = conn.cursor()
        added_record = add_recommend_request(cursor, json.loads(request))

        send_queue(added_record)

        conn.commit()
        cursor.close()
        conn.close()

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
