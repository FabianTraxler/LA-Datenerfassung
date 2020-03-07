from flask import Blueprint, request
from backend.modules.db_handler import DB_Handler
from backend.modules.group_handler import Group_Handler
from backend.modules.event_handler import Event_Handler


db_handler = DB_Handler('backend/config/db_config.json')
group_handler = Group_Handler(db_handler)
event_handler = Event_Handler(db_handler)

group_routes = Blueprint('group_routes', __name__, template_folder='templates')

@group_routes.route('/group', methods=['POST'])
def create_group():
    args = request.form
    if group_handler.create_group(
        args['name'], 
        args['typ'], 
        args['discipline_order'], 
        args['supervisor'], 
        args['volunteers'], 
        args['password']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

@group_routes.route('/group', methods=['GET'])
def get_group():
    response = group_handler.get_available_groups()
    return {"response":response, "status":200}

@group_routes.route('/group/disciplines/<name>', methods=['GET'])   
def get_disciplines(name):
    response = group_handler.get_disciplines(name)
    return {"response":response, "status":200}

@group_routes.route('/group/points/<name>', methods=['GET'])   
def get_overall_points(name):
    response =  group_handler.get_athletes_overall_points(name)
    return {"response":response, "status":200}

@group_routes.route('/group/discipline_performance/<name>/<discipline>', methods=['GET'])   
def get_discipline_performance(name, discipline):
    response = group_handler.get_athletes_discpline_performance(name, discipline)
    return {"response":response, "status":200}



@group_routes.route('/group', methods=['PUT'])
def get_group_from_password():
    args = request.form
    response = group_handler.get_group_from_password(args['password'])
    return {"response":response, "status":200}


@group_routes.route('/group/state/<name>', methods=['GET'])   
def get_state(name):
    response = group_handler.get_state(name)
    return {"response":response, "status":200}

@group_routes.route('/group/before_discipline_info/<group_name>', methods=['GET'])
def get_before_discipline_info(group_name):
    completed_disciplines_percent, next_discipline = group_handler.get_next_discipline(group_name)
    time, venue = event_handler.get_time_and_venue(group_name, next_discipline)
    response = {
        'completed_disciplines_percent': completed_disciplines_percent,
        'next_discipline': next_discipline, 
        'time': time, 
        'venue': venue
        }
    return {"response":response, "status":200}


@group_routes.route('/group/state', methods=['POST'])   
def set_state():
    args = request.form
    if group_handler.set_state(args['name'], args['state']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}


@group_routes.route('/group/discipline_active_info/<group_name>', methods=['GET'])
def get_discipline_active_info(group_name):
    _, active_discipline = group_handler.get_next_discipline(group_name)
    discipline_typ = group_handler.get_discipline_typ(active_discipline)
    startreihenfolge = group_handler.get_athletes_starting_order(group_name, active_discipline)
    response = {
        'active_discipline': active_discipline,
        'discipline_typ': discipline_typ, 
        'startreihenfolge': startreihenfolge
        }
    return {"response":response, "status":200}


@group_routes.route('/group/discipline_completed', methods=['POST'])
def discipline_completed():
    args = request.form
    attempts = args['attempts'].split(',')
    if group_handler.discpline_completed(args['group_name'], args['discipline_name'], attempts):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

