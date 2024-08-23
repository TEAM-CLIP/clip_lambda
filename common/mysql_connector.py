import mysql.connector


class MysqlConnector:
    def __init__(self, properties):
        self.__conn = mysql.connector.connect(
            host=properties['DB_HOST'],
            user=properties['DB_USERNAME'],
            password=properties['DB_PASSWORD'],
            database=properties['DB_NAME']
        )

        self.__cursor = self.__conn.cursor()


    def __delete__(self, instance):
        self.__cursor.close()
        self.__conn.close()

    def find_one(self, query, params):
        cursor = self.__cursor
        cursor.execute(query, params)
        result = cursor.fetchone()
        return result

    def find_all(self, query, params):
        cursor = self.__cursor
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result

    def execute_one(self, query, params=None):
        cursor = self.__cursor
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        self.__conn.commit()
        return cursor.lastrowid