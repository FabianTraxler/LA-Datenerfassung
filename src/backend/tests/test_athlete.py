from modules.athlete import Athlete_Handler
from modules.group import Group_Handler
from modules.db_handler import DB_Handler
import tests.database_function as db

from tests.test_group import *

def setup(path_to_config):
    handler = DB_Handler(path_to_config)
    db.drop_tables(handler)
    db.create_tables(handler)

    group_handler = Group_Handler(handler)
    create_groups(group_handler)

    athlete_handler = Athlete_Handler(handler)

    return athlete_handler

def create_athletes(athlete_handler):
    print("Creating Registerd Athletes ...")
    athlete_handler.create_registered_athlete('g1', 'Fabian', 'Traxler', '22.03.1997', 'man')
    athlete_handler.create_registered_athlete('', 'Hannah', 'Baba', '22.03.2007', 'woman')

    print('Creating Athletes ...')
    athlete_handler.create_athlete(2, 'g1', 'Fabian', 'Traxler', '22.03.1997', 'man')
    athlete_handler.create_athlete(1, 'g1', 'Elke', 'Traxler', '13.05.1969', 'woman')
    athlete_handler.create_athlete(3, 'g1', 'Fritz', 'Fischer', '22.03.1980', 'man')

    print("Creating Underaged Athletes ...")
    athlete_handler.create_athlete(4, '', 'Fabian', 'Traxler', '22.03.2016', 'man')
    athlete_handler.create_athlete(5, '', 'Hannah', 'Baba', '22.03.2007', 'woman')

def test_athlete_search_update(athlete_handler):
    print('List all athletes: ')
    print(athlete_handler.get_athletes(''))

    print('Update Athltes...')
    athlete_handler.update_athlete(3, 'first_name', 'Franz')
    athlete_handler.update_athlete(3, 'birthday', '22.01.1960')

    print('List all athletes with "Tr" in der Name: ')
    print(athlete_handler.get_athletes('Tr'))

def test_performacce(athlete_handler):
    print("Get the performance of Athlete with #1:")
    print(athlete_handler.get_athlete_performance(1))


if __name__ == '__main__':
    athlete_handler = setup("config/db_config.json")

    create_athletes(athlete_handler)
    test_athlete_search_update(athlete_handler)

    attempts = ['11.97', '13.54', '12.55']
    db.insert_achievements_100_Meter(attempts)

    test_performacce(athlete_handler)