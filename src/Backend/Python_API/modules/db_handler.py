import psycopg2
import json


class DB_Handler():
    def __init__(self, db_config_file):
        with open(db_config_file) as config_file:
            config = json.load(config_file)
    
        self.connection = psycopg2.connect(
            database=config['Database'], 
            user=config['User'], 
            password=config['Password'], 
            host=config['Host'], 
            port=config['Port'])
        
        self.cursor = self.connection.cur()


    def get_results(self, SQL_statement):
        self.cursor.execute(SQL_statement)
        rows = self.cursor.fetchall()
        return rows
    
    def get_result(self, SQL_statement):
        self.cursor.execute(SQL_statement)
        row = self.cursor.fetchone()
        return row

    def commit_statement(self, SQL_statement):
        self.cursor.execute(SQL_statement)
        self.connection.commit()
        return "Success"