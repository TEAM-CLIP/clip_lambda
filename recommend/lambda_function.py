import json
import os

import common.secret_manager as secret_manager
import common.mysql_connector as mysql_connector
import recommend_query
import common.response as response
import common.http as http
import common.sqs_helper as sqs_helper


def convert_snap_types(type_array):
    snap_type = {
        0: "개인 스냅",
        1: "우정 / 단체",
        2: "커플 / 결혼"
    }
    users_snap_types = []
    for snap in type_array:
        users_snap_types.append(snap_type[snap])
    return users_snap_types


def initialize_table(connector):
    connector.execute_one(recommend_query.create_table_query)


def add_recommend_request(connector, message):
    initialize_table(connector)
    snap_types = []
    if 'snap_types' in message:
        snap_types = message['snap_types']
    return connector.execute_one(
        recommend_query.insert_query,
        (message['phone_number'], message['prefer_style'], json.dumps(convert_snap_types(snap_types)))
    )


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
    sqs_helper.SQSSender().send_message(queue_url=os.environ['SLACK_SQS_URL'], message=message)


def handler(event, context):
    try:
        body = http.HttpRequestParser.parse_body(event, is_json=True)
        print(event)
        print(body)
        db_properties = secret_manager.get_secret_properties("chiksnap/db")
        connector = mysql_connector.MysqlConnector(db_properties)

        added_record_id = add_recommend_request(connector, body)
        send_queue(added_record_id)

        return response.ResponseBuilder.status_200(body={
            "record_id": added_record_id
        }).to_dict()

    except Exception as e:
        response.ResponseBuilder.status_500(body={
            'message': str(e)
        }).to_dict()
