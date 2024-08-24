import os
import json
import requests
import common.secret_manager as secret_manager
import common.mysql_connector as mysql_connector

class Recommend:
    def __init__(self, record_properties):
        self.record_id = record_properties[0]
        self.phone_number = record_properties[1]
        self.prefer_style = record_properties[2]

class RecommendRepository:
    def __init__(self, connector):
        self.__connector = connector

        self.__find_by_id_query = "select * from recommend_request where id = %s"


    def find_by_id(self, record_id):
        query = self.__find_by_id_query
        result = self.__connector.find_one(query, (record_id,))
        return Recommend(result)


class RecommendMessageHandler:
    def __init__(self):
        self.__slack_url = os.environ['RECOMMEND_SLACK_URL']

    def __call__(self, message):
        self.handle(message)


    def handle(self, message):
        record_id = message['record_id']

        db_properties = secret_manager.get_secret_properties("chiksnap/db")
        connector = mysql_connector.MysqlConnector(db_properties)

        recommend_repository = RecommendRepository(connector)

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

        requests.post(self.__slack_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})