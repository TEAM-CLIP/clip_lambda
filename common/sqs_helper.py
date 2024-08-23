import json
import boto3


class SQSMetaData:
    def __init__(self, event):
        self.event = event
        self.records = event['Records']

    def get_meta_data(self, is_json = False):
        for record in self.records:
            yield SQSMessage(record, is_json)


class SQSMessage:
    def __init__(self, record, is_json):
        self.record = record
        self.body = json.loads(record['body']) if is_json else record['body']


class SQSSender:
    def __init__(self):
        self.__sqs_client = boto3.client("sqs")

    def send_message(self, queue_url, message):
        self.__sqs_client.send_message(QueueUrl = queue_url, MessageBody = message)
