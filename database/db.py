import mysql.connector  # pip install mysql-connector-python
import os


class DB:

    def __enter__(self):
        print(f'Connecting to the {self._env} database on {self._host}/{self._database}:{self._port} with user {self._user}')
        self._connection = mysql.connector.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database
        )
        self._my_cursor = self._connection.cursor()
        return self

    def __exit__(self, *_):
        self._connection.close()
        self._my_cursor = None

    def __init__(self, env):

        self._my_cursor = None
        self._env = env

        if self._env == "dev" or env == "local":
            self._host = os.environ['LOCAL_DATABASE_HOST']
            self._port = os.environ['LOCAL_DATABASE_PORT']
            self._database = os.environ['LOCAL_DATABASE_NAME']
            self._user = os.environ['LOCAL_DATABASE_USER']
            self._password = os.environ['LOCAL_DATABASE_PASSWORD']

        elif self._env == "test":
            self._host = os.environ['TEST_DATABASE_HOST']
            self._port = os.environ['TEST_DATABASE_PORT']
            self._database = os.environ['TEST_DATABASE_NAME']
            self._user = os.environ['TEST_DATABASE_USER']
            self._password = os.environ['TEST_DATABASE_PASSWORD']

        elif self._env == "prod":
            self._host = os.environ['PROD_DATABASE_HOST']
            self._port = os.environ['PROD_DATABASE_PORT']
            self._database = os.environ['PROD_DATABASE_NAME']
            self._user = os.environ['PROD_DATABASE_USER']
            self._password = os.environ['PROD_DATABASE_PASSWORD']

        else:
            raise ValueError("Invalid environment.")

    def execute_query(self, query):
        if self._my_cursor is None:
            raise ValueError("Dont query unless you connect")

        print(query)
        self._my_cursor.execute(query)
        columns = [i[0] for i in self._my_cursor.description]
        return self._my_cursor.fetchall(), columns
