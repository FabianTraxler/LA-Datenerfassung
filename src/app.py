import flask
from flask import request, send_from_directory
import os

from backend.backend_init import initialize_database

from backend.routes.group import group_routes
from backend.routes.athlete import athlete_routes
from backend.routes.achievement import achievement_routes

#from backend.routes.mobile import mobile_routes

app = flask.Flask(__name__, static_folder='frontend/build')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_rect_app(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


app.register_blueprint(group_routes)
app.register_blueprint(athlete_routes)
app.register_blueprint(achievement_routes)
#app.register_blueprint(mobile_routes)

@app.route('/database/reset', methods=['GET'])
def reset_db():
    initialize_database(delete_rows = True, fill_db=True)
    return 'OK'


if __name__ == '__main__':
    initialize_database(restart_db = True, fill_db=True)
    app.run(port=3001)
