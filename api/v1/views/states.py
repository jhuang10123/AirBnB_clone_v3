#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getAllStates():
    """Retrieves the list of all State objects"""
    all_obj = storage.all('State')
    for item in all_obj.values():
        return jsonify(item.to_dict())

#Retrieves a State object: GET /api/v1/states/<state_id>
@app.route('/states/<int:state_id>', strict_slashes=False, methods=['GET'])
def GET_state(state_id):
    """GET State object, else raise 404"""
    try:
        state = storage.get("State", state_id)
    except:
        raise(404)

@app.route('states/<int:state_id>', strict_slashes=False, methods=['DELETE'])
def DEL_state(state_id):
    """DELETE State object, else raise 404, return status code 200"""

    #if keyword == 'DELETE':
        state.delete()
        storage.save()
        return #empty dictionary, 200

@app.route('states/<int:state_id>', strict_slashes=False, methods=['POST'])
def POST_state(state_id):
    """POST State object adds state, raise 400 if not valid json"""

    flask_to_dict = request.get_json
    if not flask_to_dict:
        return #...(Error: Not a JSON), 400
    name = flask_to_dict.get('name', "")
        return #...(Error: Missing name), 400

    # must return new state...continued

    flask_to_dict.pop("id", None)
    flask_to_dict.pop("created_at", None)
    flask_to_dict.pop("updated_at", None)
