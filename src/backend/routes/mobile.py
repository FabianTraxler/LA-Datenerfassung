from flask import Blueprint, request
from backend.modules.db_handler import DB_Handler
from backend.modules.group_handler import Group_Handler
from backend.modules.event_handler import Event_Handler

db_handler = DB_Handler('backend/config/db_config.json')
group_handler = Group_Handler(db_handler)
event_handler = Event_Handler(db_handler)

mobile_routes = Blueprint('mobile_routes', __name__, template_folder='templates')


@mobile_routes.route('/group', methods=['PUT'])
def get_group_from_password():
    args = request.form
    response = group_handler.get_group_from_password(args['password'])
    return {"response":response, "status":200}


@mobile_routes.route('/group/state/<name>', methods=['GET'])   
def get_state(name):
    response = group_handler.get_state(name)
    return {"response":response, "status":200}

@mobile_routes.route('/group/before_discipline_info/<group_name>', methods=['GET'])
def get_before_discipline_info(group_name):
    completed_disciplines, next_discipline = group_handler.get_next_discipline(group_name)
    time, venue = event_handler.get_time_and_venue(group_name, next_discipline)
    response = {
        'completed_disciplines': completed_disciplines,
        'next_discipline': next_discipline, 
        'time': time, 
        'venue': venue
        }
    return {"response":response, "status":200}


@mobile_routes.route('/group/state', methods=['POST'])   
def set_state():
    args = request.form
    if group_handler.set_state(args['name'], args['state']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}


@mobile_routes.route('/group/discipline_active_info/<group_name>', methods=['GET'])
def get_discipline_active_info(group_name):
    _, active_discipline = group_handler.get_next_discipline(group_name)
    discipline_typ = group_handler.get_discipline_typ(active_discipline)
    startreihenfolge = group_handler.get_athletes_starting_order(group_name)
    response = {
        'active_discipline': active_discipline,
        'discipline_typ': discipline_typ, 
        'startreihenfolge': startreihenfolge
        }
    return {"response":response, "status":200}


@mobile_routes.route('/group/discipline_completed', methods=['POST'])
def discipline_completed():
    args = request.form
    attempts = ast.literal_eval(args['attempts'])
    if group_handler.discpline_completed(
        args['name'], 
        args['discipline'], 
        attempts):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

