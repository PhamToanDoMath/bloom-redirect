from sqlite3 import Error
from sqlite.query import create_connection, create_tables, insert_mock_data


class DatabaseConnection:
    
    def __init__(self, db_file) -> None:
        self.connection  = create_connection(db_file)
        if not self.connection:
            create_tables(self.connection)
            insert_mock_data(self.connection)
    
    def execute(self, query):
        try:
            c = self.connection.cursor()
            return c.execute(query)
        except Error as e:
            print(e)