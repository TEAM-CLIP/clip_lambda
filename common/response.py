import json

class ResponseBuilder:

    @staticmethod
    def status_200(body):
        return Response(200,body)

    @staticmethod
    def status_500(body):
        return Response(500,body)


class Response:
    def __init__(self,status_code,body):
        self.status_code = status_code
        self.body: dict = body

    def to_dict(self):
        return {
            'statusCode': self.status_code,
            'body': self.body
        }

    def to_json(self):
        return json.dumps(self.to_dict())