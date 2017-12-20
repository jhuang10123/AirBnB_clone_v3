#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getAllStates():
    """Retrieves the list of all State objects"""
    all_states = storage.all('State')
    for item in all_states.values():
        return jsonify(item.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'DELETE'])
def get_state():
    if request.method == 'GET':
        def GET_state(state_id):
            """GET State object, else raise 404"""
            #get all State objects
            all_states = storage.all('State')
            for item in all_states.values():
                if state_id == item.id:
                    return jsonify(item.to_dict())
                    abort(404)

    elif request.method == 'DELETE':
        state = storage.get('State', state_id)
        if state is None:
            abort(404)
        state.delete()
        state.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_state():
    """adds state, raise 400 if not valid json"""

# get user data
# get_json method parses the incoming JSON request data and returns it as aPython dictionary.

    post_content = request.get_json()
# Post_content example:
# {"name":"washington"}


#return error if not valid json format
    if not request.is_json: 
        abort(400, "Not a JSON")


#return error if user input doesnt include the key 'name'
    name = post_content.get('name')
    if not name:
        abort(400, "Missing name")

#create a new state with user content
#send in user input(key:value) to create new object
    new_state = State(**post_content)
    storage.new(new_state)

#save new object
    new_state.save()

    return jsonify(new_state.to_dict()), 201

