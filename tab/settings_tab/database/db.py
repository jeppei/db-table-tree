import logging
import warnings
from tkinter import messagebox
import mysql.connector  # pip install mysql-connector-python
from tab.settings_tab.database_connection_settings import DatabaseConnectionSettings
import os
from sqlalchemy import create_engine, MetaData

# Suppress SQLAlchemy warnings about column types it doesn't recognize
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.captureWarnings(True)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


def read_setting(param):
    if param[0] == "$":
        return os.environ.get(param[1:])
    else:
        return param


class DB:

    def __enter__(self):

        self.name = read_setting(self.database_connection_settings.name.get())
        self.host = read_setting(self.database_connection_settings.host.get())
        self.port = read_setting(self.database_connection_settings.port.get())
        self.user = read_setting(self.database_connection_settings.user.get())
        self.password = read_setting(self.database_connection_settings.password.get())
        self.database = read_setting(self.database_connection_settings.database.get())
        self.table_to_column_dict = self.get_table_and_columns()

        print(
            f'Connecting to the {self.name} '
            f'database on {self.host}/'
            f'{self.database}:'
            f'{self.port} '
            f'with user {self.user}'
        )
        self._connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self._my_cursor = self._connection.cursor()
        return self

    def __exit__(self, *_):
        self._connection.close()
        self._my_cursor = None

    def __init__(self, database_connection_settings: DatabaseConnectionSettings):
        self.database_connection_settings = database_connection_settings

    def execute_query(self, query):
        if self._my_cursor is None:
            raise ValueError("Dont query unless you connect")

        print(query)
        try:
            self._my_cursor.execute(query)
        except mysql.connector.Error as error:
            if error.errno == 1146 and error.sqlstate == '42S02':
                messagebox.showinfo("The table doesnt exist", "The selected table doesn't exist!")
                return [], []
            else:
                messagebox.showinfo(
                    "Unknown error", "Unknown error while trying to execute the query\n\n" + query + "\n\n" + error.msg
                )
                return [], []

        columns = [i[0] for i in self._my_cursor.description]
        return self._my_cursor.fetchall(), columns

    def get_table_and_columns(self):
        engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}')

        metadata = MetaData()
        metadata.reflect(bind=engine)

        table_names = metadata.tables.keys()
        table_to_columns = {}
        for table_name in table_names:
            table = metadata.tables[table_name]
            columns = [column.key for column in table.columns]
            table_to_columns[table_name] = columns
        return table_to_columns
