import sqlite3
from sqlite3 import Error

sql_create_registerdUrl_table = """ 
    CREATE TABLE IF NOT EXISTS registeredUrl (
        id integer PRIMARY KEY,
        serverName text NOT NULL,
        url text NOT NULL
    ); 
"""

sql_insert_mock_data = """ 
    INSERT INTO registeredUrl (serverName, url) VALUES ('apple', 'http://localhost:9999'); 
    INSERT INTO registeredUrl (serverName, url) VALUES ('microsoft', 'http://localhost:9998'); 
    INSERT INTO registeredUrl (serverName, url) VALUES ('deepmind', 'http://localhost:9997'); 
"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def execute(connection, sql):
    try:
        c = connection.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def create_tables(connection):
    return execute(connection, sql_create_registerdUrl_table)
        
def insert_mock_data(connection):
    execute(connection,sql_insert_mock_data)
        
