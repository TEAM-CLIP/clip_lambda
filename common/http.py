import json

class HttpRequestParser:

    @staticmethod
    def parse_body(request, is_json=False):
        if is_json:
            return json.loads(request['body'])
        return request['body']