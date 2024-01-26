import logging
import traceback
import warnings
from tkinter import messagebox
import tkinter as tk
import mysql.connector  # pip install mysql-connector-python
from tab.settings_tab.database_connection_settings import DatabaseConnectionSettings
import os
from sqlalchemy import create_engine, MetaData

# Suppress SQLAlchemy warnings about column types it doesn't recognize
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.captureWarnings(True)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


def read_setting(param):
    if param[0] == '$':
        return os.environ.get(param[1:])
    else:
        return param


class DB:

    def __init__(self, database_connection_settings: DatabaseConnectionSettings):
        self.database_connection_settings = database_connection_settings

        self.name = read_setting(self.database_connection_settings.name.get())
        self.host = read_setting(self.database_connection_settings.host.get())
        self.port = read_setting(self.database_connection_settings.port.get())
        self.user = read_setting(self.database_connection_settings.user.get())
        self.password = read_setting(self.database_connection_settings.password.get())
        self.database = read_setting(self.database_connection_settings.database.get())

        self.table_to_column_dict = self.get_table_and_columns()

    def __str__(self):
        return(
            f'connection details:\n'
            f' - host: {self.host}\n'
            f' - database: {self.database}\n'
            f' - port: {self.port}\n'
            f' - user: {self.user}\n'
            f' - password is not None: {self.password is not None}\n'
        )

    def __enter__(self):


        #self.table_to_column_dict = {}
        #self.connected = False
        #self._connection = None

        print(f'Connecting to the {self.name} with {self}')
        self._connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self._my_cursor = self._connection.cursor()
        #try:
        #    self._connection = mysql.connector.connect(
        #        host=self.host,
        #        port=self.port,
        #        user=self.user,
        #        password=self.password,
        #        database=self.database
        #    )
        #    self._my_cursor = self._connection.cursor()
        #    self._my_cursor.execute('SELECT 1')
        #    self.table_to_column_dict = self.get_table_and_columns()
        #    self.connected = True
        #except Exception as e:
        #    self.show_connection_error_popup(e)
        #    self.connected = False

        return self

    def __exit__(self, *_):
        self._connection.close()
        #if self._connection is not None:
        #    self._connection.close()
        self._my_cursor = None

    def show_connection_error_popup(self, error_message: Exception):
        root = tk.Tk()
        root.withdraw()
        message = (
            f'Failed to connect to the database using:\n'
            f' - host={self.host}\n'
            f' - port={self.port}\n'
            f' - user={self.user}\n'
            f' - password=***\n'
            f' - database={self.database}\n'
            f'\n'
            f'{str(error_message)}'
        )
        print(message)
        #traceback.print_exc()
        tk.messagebox.showinfo('Connection Error', message)
        root.destroy()

    def execute_query(self, query):
        if self._my_cursor is None:
            raise ValueError('Dont query unless you connect')
        #if not self.connected or self._my_cursor is None:
        #    return [], []

        print(query)
        try:
            self._my_cursor.execute(query)
        except mysql.connector.Error as error:
            if error.errno == 1146 and error.sqlstate == '42S02':
                messagebox.showinfo('The table doesnt exist', 'The selected table doesnt exist!')
                return [], []
            else:
                messagebox.showinfo(
                    'Unknown error', 'Unknown error while trying to execute the query\n\n' + query + '\n\n' + error.msg
                )
                return [], []

        columns = [i[0] for i in self._my_cursor.description]
        return self._my_cursor.fetchall(), columns


    def get_table_and_columns(self):
        try:
            connection_string = f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
            print(f'Connecting with {self}')
            print(f'Connection string: {connection_string}')
            engine = create_engine(connection_string)
            #engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}')

            metadata = MetaData()
            metadata.reflect(bind=engine)

            table_names = metadata.tables.keys()
            table_to_columns = {}
            for table_name in table_names:
                table = metadata.tables[table_name]
                columns = [column.key for column in table.columns]
                table_to_columns[table_name] = columns
            return table_to_columns

        except Exception as ex:
            print('Failed to get tables and columns')
            return{}
