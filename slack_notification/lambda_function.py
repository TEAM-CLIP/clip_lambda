import json
import os

import requests

import common.secret_manager as secret_manager
import common.mysql_connector as mysql_connector
import common.sqs_helper as sqs_helper
import recommend.recommend as recommend
import common.response as response



def send_message(record_id, webhook_url):
    db_properties = secret_manager.get_secret_properties("chiksnap/db")
    connector = mysql_connector.MysqlConnector(db_properties)

    recommend_repository = recommend.RecommendRepository(connector)

    result = recommend_repository.find_by_id(record_id)
    phone_number = result.phone_number
    prefer_style = result.prefer_style

    data = {
        'text': f"""
        새로운 추천 요청이 들어왔어요! 🎉
        - 전화번호: {phone_number}
        - 선호 스타일: {prefer_style}
        """.strip()
    }

    requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})


def handler(event, context):
    try:
        webhook_url = os.environ['RECOMMEND_SLACK_URL']

        meta_datas = sqs_helper.SQSMetaData(event)
        for meta_data in meta_datas.get_meta_data(is_json=True):
            data = meta_data.body['body']
            record_id = data['record_id']
            send_message(record_id, webhook_url)

    except Exception as e:
        return response.ResponseBuilder.status_500(body = {
            'message': str(e)
        }).to_dict()

    return response.ResponseBuilder.status_200(body = {
        'message': 'success'
    }).to_dict()
