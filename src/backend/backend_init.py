import flask
from flask import request

from backend.modules.db_handler import DB_Handler
from backend.modules.group_handler import Group_Handler
from backend.modules.athlete_handler import Athlete_Handler
from backend.modules.achievement_handler import Achievement_Handler
from backend.modules.event_handler import Event_Handler

from backend.routes.group import group_routes
from backend.routes.athlete import athlete_routes

def drop_tables(handler):
    query = """drop table achievements;
    drop table athletes;
    drop table registered_athletes;
    drop table events;
    drop table groups;
    """

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
        lauf_bahn VARCHAR(6),
        attempts VARCHAR(250),
        best_attempt VARCHAR(50),
        PRIMARY KEY (athlete_number, discipline_name)
    );

    CREATE TABLE events(
        group_name VARCHAR(20) REFERENCES groups(name),
        discipline_name VARCHAR(20),
        starting_time VARCHAR(20),
        venue VARCHAR(30),
        PRIMARY KEY(group_name, discipline_name)
    );"""
    handler.commit_statement(query)

def create_groups(group_handler):
    print('Creating groups ...')
    for i in range(1,11):
        group_handler.create_group('Gruppe {}'.format(i), 'Decathlon', 'Normal', 'Fabian', 'Fabian', '{}'.format(i))
   
    for i in range(4,17, 2):
        group_handler.create_group('U{}'.format(i), 'Triathlon', 'Normal', 'Fabian', 'Fabian', 'U{}'.format(i))

def create_events(event_handler):
    event_handler.store_event('Gruppe 1', '100-Meter', '8:00', 'Laufbahn')
    event_handler.store_event('Gruppe 1', 'Weitprung', '8:30', 'Weit 1')
    event_handler.store_event('Gruppe 1', 'Kugel-Stoßen', '10:15', 'Kugel 2')
    event_handler.store_event('Gruppe 1', 'Hochsprung', '11:15', 'Hoch 2')

    event_handler.store_event('Gruppe 2', '100-Meter', '8:30', 'Laufbahn')
    event_handler.store_event('Gruppe 2', 'Diskus', '9:00', 'Weit 2')
    event_handler.store_event('Gruppe 2', 'Stabhochsprung', '10:45', 'Stab 1')

def insert_athletes(athlete_handler):
    print('Creating Athletes ...')
    athlete_handler.create_athlete(2, 'Gruppe 1', 'Fabian', 'Traxler', '22.03.1997', 'man')
    athlete_handler.create_athlete(1, 'Gruppe 1', 'Elke', 'Traxler', '13.05.1969', 'woman')
    athlete_handler.create_athlete(3, 'Gruppe 1', 'Fritz', 'Fischer', '22.03.1980', 'man')
    for i in range(4,30):
        gender = 'man' if i % 2 == 0 else 'woman'
        athlete_handler.create_athlete(i, 'Gruppe 2', 'Test_' + str(i), 'Traxler', '22.03.' + str(1970 - i), 'man')


def insert_achievements_100_Meter(achievement_handler, attempts):
    print('Creating 100-Meter Results ...')
    for x in range(len(attempts)): # number of athletes
        achievement_handler.store_attempt(x + 1, 'Gruppe 1', '100-Meter', attempts[x])
    achievement_handler.store_result('100-Meter', 'Gruppe 1', attempts)

def insert_achievements_Weitsprung(achievement_handler, attempts):
    print('Inserting Weitsprung Results ...')

    for i in range(3): #number of attempts
        for x in range(len(attempts)): # number of athletes
            achievement_handler.store_attempt(x + 1, 'Gruppe 1', 'Weitsprung', attempts[x].split('/')[i])

    achievement_handler.store_result('Weitsprung', 'Gruppe 1', attempts)

    return attempts

def delete_all_rows(db_handler):
    query = 'DELETE FROM achievements; DELETE FROM events; DELETE FROM athletes; DELETE FROM groups;'
    db_handler.commit_statement(query)


def initialize_database(restart_db = False, delete_rows = False, fill_db = False):

    db_handler = DB_Handler('backend/config/db_config.json')

    if restart_db:
        drop_tables(db_handler)
        create_tables(db_handler)
    
    if delete_rows:
        delete_all_rows(db_handler)

    if fill_db:
        group_handler = Group_Handler(db_handler)
        athlete_handler = Athlete_Handler(db_handler)
        achievement_handler = Achievement_Handler(db_handler)
        event_handler = Event_Handler(db_handler)

        create_groups(group_handler)
        group_handler.set_state('Gruppe 9', 'final')
        create_events(event_handler)
        insert_athletes(athlete_handler)
        attempts_100_Meter = ['11.97', '13.54', '12.55']
        insert_achievements_100_Meter(achievement_handler, attempts_100_Meter)
        group_handler.discpline_completed('Gruppe 1', '100-Meter', attempts_100_Meter)
        attempts_Weitsprung = ['4.22/4.20/4.43', '3.23/6.32/5.23', '5.34/4.67/4.45']
        insert_achievements_Weitsprung(achievement_handler, attempts_Weitsprung)
        group_handler.discpline_completed('Gruppe 1', 'Weitsprung', attempts_Weitsprung)
        group_handler.set_state('Gruppe 1', 'discipline_active')
