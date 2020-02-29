from modules.db_handler import DB_Handler
from modules.athlete import Athlete_Handler
from modules.achievement import Achievement_Handler

db_handler = DB_Handler("config/db_config.json")
athlete_hanlder = Athlete_Handler(db_handler)
achievement_handler = Achievement_Handler(db_handler)

def drop_tables(handler):
    query = """drop table achievements;
    drop table athletes;
    drop table registered_athletes;
    drop table groups;"""

    handler.commit_statement(query)

def create_tables(handler):
    query = """CREATE TABLE groups(
        name VARCHAR(20) PRIMARY KEY,
        type VARCHAR(15),
        discipline_order VARCHAR(10),
        state VARCHAR(20),
        completed_disciplines INTEGER,
        supervisor VARCHAR(40),
        volunteers VARCHAR(200),
        password_hash VARCHAR(256)
    );

    CREATE TABLE athletes(
        number INTEGER PRIMARY KEY,
        group_name VARCHAR(20) REFERENCES groups(name),
        first_name VARCHAR(30),
        last_name VARCHAR(30),
        birthday VARCHAR(30),
        age_group VARCHAR(4),
        gender VARCHAR(6)
    );


    CREATE TABLE registered_athletes(
        group_name VARCHAR(20) REFERENCES groups(name),
        first_name VARCHAR(30),
        last_name VARCHAR(30),
        birthday VARCHAR(30),
        age_group VARCHAR(4),
        gender VARCHAR(6),
        PRIMARY KEY (first_name, last_name)
    );

    CREATE TABLE achievements(
        athlete_number INTEGER REFERENCES athletes(number),
        discipline_name VARCHAR(20),
        points INTEGER,
        group_name VARCHAR(20) REFERENCES groups(name),
        attempts VARCHAR(250),
        best_attempt VARCHAR(50),
        PRIMARY KEY (athlete_number, discipline_name)
    );"""
    handler.commit_statement(query)

def insert_athletes(handler):
    athlete_hanlder.create_athlete(2, 'g1', 'Fabian', 'Traxler', '22.03.1997', 'man')
    athlete_hanlder.create_athlete(1, 'g1', 'Elke', 'Traxler', '13.05.1969', 'woman')
    athlete_hanlder.create_athlete(3, 'g1', 'Fritz', 'Fischer', '22.03.1980', 'man')

def insert_achievements_100_Meter(attempts):
    for x in range(len(attempts)): # number of athletes
        achievement_handler.store_attempt(x + 1, 'g1', '100-Meter', attempts[x])
    achievement_handler.store_result('100-Meter', 'g1', attempts)


def insert_achievements_Weitsprung(attempts):
    for i in range(3): #number of attempts
        for x in range(len(attempts)): # number of athletes
            achievement_handler.store_attempt(x + 1, 'g1', 'Weitsprung', attempts[x].split('/')[i])
    achievement_handler.store_result('Weitsprung', 'g1', attempts)

