import psycopg2
import json


class DB_Handler():
    """Interface to the Postgres Database 
    ...
    Methods
    -------
    get_results(SQL_Statement)
        Gets the results of the provided SQL Statement
        Returns a list of tuples or an empty list

    get_result(SQL_Statement)
        Gets the result of the provided SQL Statement
        Returns a single tuple or None

    commit_statement(SQL_Statement)
        Commits a SQL Statement to the database
        Returns 1 if "Success" or 0 if "Failed"
    """

    def __init__(self, db_config_file):
        """
        Parameters
        ----------
        db_config_file : str
            Path to the Database Configuration File
        """

        with open(db_config_file) as config_file:
            config = json.load(config_file)
    
        self.connection = psycopg2.connect(
            database=config['Database'], 
            user=config['User'], 
            password=config['Password'], 
            host=config['Host'], 
            port=config['Port'])
        
        self.cursor = self.connection.cursor()

    def get_results(self, SQL_statement):
        """Gets the results of the provided SQL Statement

        Returns a list of tuples or an empty list
        """
        try:
            self.cursor.execute(SQL_statement)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(e)
            return []
        
    def get_result(self, SQL_statement):
        """Gets the result of the provided SQL Statement

        Returns a single tuple or None
        """
        try:
            self.cursor.execute(SQL_statement)
            row = self.cursor.fetchone()
            return row
        except Exception as e:
            print(e)
            return ()

    def commit_statement(self, SQL_statement):
        """Commits a SQL Statement to the database

        Returns 1 if "Success" or 0 if "Failed
        """
        try:
            self.cursor.execute(SQL_statement)
            self.connection.commit()
            return 1
        except Exception as e:
            print(e)
            return 0

    def close_connection(self):
        """Close the connection to the database"""

        self.connection.close()
        return
        