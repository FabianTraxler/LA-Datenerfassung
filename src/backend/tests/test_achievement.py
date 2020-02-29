from modules.group import Group_Handler
from modules.achievement import Achievement_Handler, Points_Calculator
from modules.db_handler import DB_Handler
import tests.database_function as db

def setup(path_to_config):

    handler = DB_Handler(path_to_config)

    db.drop_tables(handler)
    db.create_tables(handler)

    group_handler = Group_Handler(handler)


    print('Creating a group ...')
    group_handler.create_group('g1', 'Decathlon', 'Normal', 'Fabian', 'Fabian', 'Gruppe1')

    print('Inserting Athletes ...')
    db.insert_athletes(handler)

    achievement_handler = Achievement_Handler(handler)

    return achievement_handler

def insert_100_Meter(achievement_handler):
    print('Inserting 100-Meter Results ...')
    attempts_100_Meter = ['11.97', '13.54', '12.55']

    for x in range(len(attempts_100_Meter)): # number of athletes
        achievement_handler.store_attempt(x + 1, 'g1', '100-Meter', attempts_100_Meter[x])

    achievement_handler.store_result('100-Meter', 'g1', attempts_100_Meter)

    return attempts_100_Meter

def insert_Weitsprung(achievement_handler):
    print('Inserting Weitsprung Results ...')
    attempts_Weitsprung = ['4.22/4.20/4.43', '3.23/6.32/5.23', '5.34/4.67/4.45']

    for i in range(3): #number of attempts
        for x in range(len(attempts_Weitsprung)): # number of athletes
            achievement_handler.store_attempt(x + 1, 'g1', 'Weitsprung', attempts_Weitsprung[x].split('/')[i])

    achievement_handler.store_result('Weitsprung', 'g1', attempts_Weitsprung)

    return attempts_Weitsprung

def insert_Hochsprung(achievement_handler):
    print('Inserting Hochsprung Results ...')
    achievement_handler.set_starting_height(1, 'g1', 'Hochsprung', 80)
    achievement_handler.set_starting_height(2, 'g1', 'Hochsprung', 132)
    achievement_handler.set_starting_height(3, 'g1', 'Hochsprung', 120)

    attempts_Hochsprung = ['O/O/XO/O/XXX', '-/-/-/-/-/-/-/-/-/-/-/-/-/XXO/XO/O/XXX', '-/-/-/-/-/-/-/-/-/-/XO/XXX']

    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(1, 'g1', 'Hochsprung', 'X')


    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Hochsprung', 'X')

    achievement_handler.store_attempt(3, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(3, 'g1', 'Hochsprung', 'O')
    achievement_handler.store_attempt(3, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(3, 'g1', 'Hochsprung', 'X')
    achievement_handler.store_attempt(3, 'g1', 'Hochsprung', 'X')

    achievement_handler.store_result('Hochsprung', 'g1', attempts_Hochsprung)

    return attempts_Hochsprung

def insert_Stabhochsprung(achievement_handler):
    print('Inserting Stabhochsprung Results ...')

    achievement_handler.set_starting_height(1, 'g1', 'Stabhochsprung', 140)
    achievement_handler.set_starting_height(2, 'g1', 'Stabhochsprung', 200)
    achievement_handler.set_starting_height(3, 'g1', 'Stabhochsprung', 160)

    attempts_Stabhochsprung = ['-/O/XO/O/XXX', '-/-/-/-/XXO/XO/O/XXX', '-/-/XO/XXX']

    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(1, 'g1', 'Stabhochsprung', 'X')


    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(2, 'g1', 'Stabhochsprung', 'X')

    achievement_handler.store_attempt(3, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(3, 'g1', 'Stabhochsprung', 'O')
    achievement_handler.store_attempt(3, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(3, 'g1', 'Stabhochsprung', 'X')
    achievement_handler.store_attempt(3, 'g1', 'Stabhochsprung', 'X')

    achievement_handler.store_result('Stabhochsprung', 'g1', attempts_Stabhochsprung)
    return attempts_Stabhochsprung

if __name__ == '__main__':
    achievement_handler = setup("config/db_config.json")

    insert_100_Meter(achievement_handler)

    insert_Weitsprung(achievement_handler)

    insert_Hochsprung(achievement_handler)

    insert_Stabhochsprung(achievement_handler)