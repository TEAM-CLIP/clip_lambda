import recommend.recommend as recommend
import pre_registration.pre_registration as registration

class MessageHandler:
    def __init__(self):
        self.support_message_types = {
            "photographer_recommend": recommend.RecommendMessageHandler(),
            "pre_registration": registration.RegistrationMessageHandler()
        }


    def handle(self, message):
        message_type = message['message_type']
        if message_type not in self.support_message_types:
            raise Exception(f"Unsupported message type: {message_type}")

        self.support_message_types[message_type](message['body'])

