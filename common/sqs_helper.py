import json


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