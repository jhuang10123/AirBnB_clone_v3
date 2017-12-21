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
    retval = []
    all_states = storage.all('State')
    for item in all_states.values():
        retval.append(item.to_dict())
    return jsonify(retval)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def GET_state(state_id):
    """GET State object, else raise 404"""

    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def DEL_state(state_id):
    """ delete a state object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_state():
    """adds state, raise 400 if not valid json"""
    post_content = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    name = post_content.get('name')
    if not name:
        abort(400, "Missing name")

# send in user input(key:value) to create new object
    new_state = State(**post_content)
    storage.new(new_state)

    new_state.save()
    storage.close()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def PUT_state(state_id):
    """ """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]

# get content to update
# key:value
# {"name":"California is cool"}
    content = request.get_json()

    if not request.is_json:
        abort(404, "Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(state, key, val)

    state.save()
    storage.close()

    return jsonify(state.to_dict())
