import json
import os

import mysql.connector
import boto3
from mysql.connector import custom_error_exception

import common.secret_manager as secret_manager
import common.mysql_connector as mysql_connector
import recommend_query



def initialize_table(connector):
    connector.execute_one(recommend_query.create_table_query)


def add_recommend_request(connector, message):
    initialize_table(connector)
    return connector.execute_one(recommend_query.insert_query, (message['phone_number'], message['prefer_style']))

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
        request  = json.dumps(event)
        db_properties = secret_manager.get_secret_properties("chiksnap/db")
        connector = mysql_connector.MysqlConnector(db_properties)

        added_record_id = add_recommend_request(connector, json.loads(request))
        send_queue(added_record_id)

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
