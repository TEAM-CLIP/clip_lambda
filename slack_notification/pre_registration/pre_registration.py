import os
import json
import requests
import common.secret_manager as secret_manager
import common.mysql_connector as mysql_connector


class Registration:
    def __init__(self, record_properties):
        self.record_id = record_properties[0]
        self.phone_number = record_properties[1]
        self.service_name = record_properties[2]


class RegistrationRepository:
    def __init__(self, connector):
        self.__connector = connector

        self.__find_by_id_query = "select id,phone_number,service_name from pre_registration_request where id = %s"

    def find_by_id(self, record_id):
        query = self.__find_by_id_query
        result = self.__connector.find_one(query, (record_id,))
        return Registration(result)


class RegistrationMessageHandler:
    def __init__(self):
        self.__slack_url = os.environ['REGISTRATION_SLACK_URL']
        self.__db_properties = secret_manager.get_secret_properties("chiksnap/db")
        self.__connector = mysql_connector.MysqlConnector(self.__db_properties)

        self.__message_format = """
        새로운 사전 신청이 들어왔어요! 🎉
        - 전화번호: {phone_number}
        - 서비스명: {service_name}
        """.strip()

    def __call__(self, message):
        self.handle(message)

    def handle(self, message):
        record_id = message['record_id']

        registration_repository = RegistrationRepository(self.__connector)

        result = registration_repository.find_by_id(record_id)
        phone_number = result.phone_number
        service_name = result.service_name

        data = {
            'text': self.__message_format.format(
                phone_number=phone_number,
                service_name=service_name,
            )
        }

        requests.post(self.__slack_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
