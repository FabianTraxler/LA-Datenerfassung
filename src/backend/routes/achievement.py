from flask import Blueprint, request
from backend.modules.db_handler import DB_Handler
from backend.modules.achievement_handler import Achievement_Handler


db_handler = DB_Handler('backend/config/db_config.json')
achievement_handler = Achievement_Handler(db_handler)


achievement_routes = Blueprint('achievement_routes', __name__, template_folder='templates')


@achievement_routes.route('/attempt', methods=['POST'])
def store_attempt():
    args = request.form
    if achievement_handler.store_attempt(
        args['athlete_number'],
        args['group_name'],
        args['discipline_name'],
        args['attempt']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

@achievement_routes.route('/result', methods=['POST'])
def store_result():
    args = request.form
    attempts = args['attempts'].split(',')
    if achievement_handler.store_result(
        args['discipline_name'],
        args['group_name'],
        attempts):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

@achievement_routes.route('/starting_height', methods=['POST'])
def store_starting_height():
    args = request.form
    if achievement_handler.set_starting_height(
        args['athlete_number'],
        args['group_name'],
        args['discipline_name'],
        int(args['height'])):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}
