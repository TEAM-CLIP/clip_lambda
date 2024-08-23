
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
