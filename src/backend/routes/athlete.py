from flask import Blueprint, request
from backend.modules.db_handler import DB_Handler
from backend.modules.athlete_handler import Athlete_Handler


db_handler = DB_Handler('backend/config/db_config.json')
athlete_handler = Athlete_Handler(db_handler)


athlete_routes = Blueprint('athlete_routes', __name__, template_folder='templates')

@athlete_routes.route('/athlete', methods=['POST'])
def create_athlete():
    args = request.form
    if athlete_handler.create_athlete(int(args['athlete_number']), args['group_name'],args['first_name'],args['last_name'],args['birthday'],args['gender']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

@athlete_routes.route('/athlete', methods=['PUT'])
def update_athlete():
    args = request.form
    if athlete_handler.update_athlete(int(args['athlete_number']), args['column'],args['new_value']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}

@athlete_routes.route('/athlete/<search_string>', methods=['GET'])
def get_athletes(search_string):
    response = athlete_handler.get_athletes(search_string)
    return {"response":response, "status":200}
    
@athlete_routes.route('/athlete/performance/<athlete_number>', methods=['GET'])
def get_athlete_performance(athlete_number):
    response = athlete_handler.get_athlete_performance(athlete_number)
    return {"response":response, "status":200}

@athlete_routes.route('/registered_athlete', methods=['POST'])
def create_registered_athlete():
    args = request.form
    if athlete_handler.create_registered_athlete(args['group_name'],args['first_name'],args['last_name'],args['birthday'],args['gender']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}
    
@athlete_routes.route('/registered_athlete/<search_string>', methods=['GET'])
def get_registered_athletes(search_string):
    response = athlete_handler.get_registered_athletes(search_string)
    return {"response":response, "status":200}

@athlete_routes.route('/registered_athlete', methods=['PUT'])
def update_registered_athlete():
    args = request.form
    if athlete_handler.update_athlete(int(args['athlete_number']), args['column'],args['new_value']):
        return {"response":'Success', "status":200}
    else:
        return {"response":'Failed', "status":400}