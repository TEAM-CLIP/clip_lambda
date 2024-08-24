import common.sqs_helper as sqs_helper
import common.response as response
from message_handler import MessageHandler


def handler(event, context):
    try:
        message_handler = MessageHandler()

        meta_datas = sqs_helper.SQSMetaData(event)
        for meta_data in meta_datas.get_meta_data(is_json=True):
            message_handler.handle(meta_data.body)

    except Exception as e:
        return response.ResponseBuilder.status_500(body = {
            'message': str(e)
        }).to_dict()

    return response.ResponseBuilder.status_200(body = {
        'message': 'success'
    }).to_dict()
