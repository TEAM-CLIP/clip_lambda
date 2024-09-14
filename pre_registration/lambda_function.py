import json
import os

import common.secret_manager as secret_manager
import common.mysql_connector as mysql_connector
import common.response as response
import common.http as http
import common.sqs_helper as sqs_helper
import pre_registration_query as pre_registration_query

def initialize_table(connector):
    connector.execute_one(pre_registration_query.create_table_query)

def add_pre_registration_request(connector, message):
    initialize_table(connector)
    return connector.execute_one(pre_registration_query.insert_query, (message['phone_number'], message['hangout']))

def create_slack_message(record_id):
    message = {
        'message_type': "pre_registration",
        'body': {
            "record_id": record_id
        }
    }

    return json.dumps(message)

def send_queue(record_id):
    message = create_slack_message(record_id)
    sqs_helper.SQSSender().send_message(queue_url = os.environ['SLACK_SQS_URL'], message = message)

def handler(event, context):
    try:
        body = http.HttpRequestParser.parse_body(event, is_json=True)
        print(event)
        print(body)
        db_properties = secret_manager.get_secret_properties("chiksnap/db")
        connector = mysql_connector.MysqlConnector(db_properties)

        added_record_id = add_pre_registration_request(connector, body)
        send_queue(added_record_id)

        return response.ResponseBuilder.status_200(body={
            "record_id": added_record_id
        }).to_dict()

    except Exception as e:
        response.ResponseBuilder.status_500(body= {
            'message': str(e)
        }).to_dict()