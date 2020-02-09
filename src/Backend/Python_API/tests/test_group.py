from modules.group import Group_Handler
from modules.db_handler import DB_Handler
import tests.database_function as db


def create_groups(group_handler):
    print('Creating groups ...')
    for i in range(1,11):
        group_handler.create_group('g{}'.format(i), 'Decathlon', 'Normal', 'Fabian', 'Fabian', 'Gruppe1')
   
    for i in range(4,17, 2):
        group_handler.create_group('U{}'.format(i), 'Triathlon', 'Normal', 'Fabian', 'Fabian', 'U{}'.format(i))

def test_group_1(group_handler):
    print('----------')
    print('Getting Group State:')
    print(group_handler.get_state('g1'))

    print('Getting Next Discipline:')
    print(group_handler.get_next_discipline('g1'))

    print('Set Group State to "discipline_active" ....')
    group_handler.set_state('g1', 'discipline_active')

    print('Getting Group State:')
    print(group_handler.get_state('g1'))

    print('Show starting order ...')
    print(group_handler.get_athletes_starting_order('g1'))


def test_group_2(group_handler):
    print('Finisching Discipline and computing Points ...')
    group_handler.discpline_completed('g1',  group_handler.get_next_discipline('g1'), attempts)
    print('State of the group: ')
    print(group_handler.get_state('g1'))

    print('Next discipline:')
    print(group_handler.get_next_discipline('g1'))

   
def test_group_3(group_handler):
    print('Finisching Discipline and computing Points ...')
    group_handler.discpline_completed('g1', group_handler.get_next_discipline('g1'), attempts)

    print('Next discipline:')
    print(group_handler.get_next_discipline('g1'))

    print('Get the overall points at this moment')
    scores = group_handler.get_athletes_overall_points('g1')
    print(scores)

    print('Show all available groups')
    print(group_handler.get_available_groups())

    print('Show all disciplines for "g1"')
    print(group_handler.get_disciplines('g1'))

    print('Show the athletes performance of Weitsprung of group 1')
    print(group_handler.get_athletes_discpline_performance('g1', 'Weitsprung'))


if __name__ == '__main__':
    handler = DB_Handler("modules/db_config.json")
    db.drop_tables(handler)
    db.create_tables(handler)

    group_handler = Group_Handler(handler)

    create_groups(group_handler)

    print('Inserting Athletes ...')
    db.insert_athletes(handler)

    test_group_1(group_handler)

    print('Inserting Achievements ...')
    attempts = ['11.97', '13.54', '12.55']
    db.insert_achievements_100_Meter(attempts)

    test_group_2(group_handler)

    print('Inserting Achievements ...')
    attempts = ['4.22/4.20/4.43', '3.23/6.32/5.23', '5.34/4.67/4.45']
    db.insert_achievements_Weitsprung(attempts)

    test_group_3(group_handler)