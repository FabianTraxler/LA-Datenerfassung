from modules.db_handler import DB_Handler
from modules.athlete import Athlete_Handler
from modules.achievement import Achievement_Handler
from modules.group import Group_Handler

from tests.test_group import *
from tests.test_athlete import *
from tests.test_achievement import *

def setup(path_to_config):
    handler = DB_Handler(path_to_config)
    db.drop_tables(handler)
    db.create_tables(handler)

    group_handler = Group_Handler(handler)
    athlete_handler = Athlete_Handler(handler)
    achievement_handler = Achievement_Handler(handler)

    return group_handler, athlete_handler, achievement_handler, handler

if __name__ == '__main__':
    group_handler, athlete_handler, achievement_handler, handler = setup("config/db_config.json")

    create_groups(group_handler)

    create_athletes(athlete_handler)

    test_group_1(group_handler)
    attempts = insert_100_Meter(achievement_handler)
    test_group_2(group_handler, attempts)

    test_group_1(group_handler)
    attempts = insert_Weitsprung(achievement_handler)
    test_group_2(group_handler, attempts)

    attempts = insert_Hochsprung(achievement_handler)

    attempts = insert_Stabhochsprung(achievement_handler)

    test_group_3(group_handler, attempts)


