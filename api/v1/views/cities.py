#!/Usr/Bin/python3
"""

"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def getAllCities(state_id):
    """ """
    city_list = []
    all_cities = storage.all('City')

    get_state = storage.get("State", state_id)
    if get_state is None:
        abort(404)

    for item in all_cities.values():
        if item.state_id == state_id:
            city_list.append(item.to_dict())

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def getCity(city_id):
    """ return city object matching city_id """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def DEL_city(city_id):
    """delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def POST_city(state_id):
    """ adds a city"""
    # user input: {"name":"San Diego"}
    post_content = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    name = post_content.get('name')
    if not name:
        abort(400, "Missing name")

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    new_city = City(**post_content)
    new_city.state_id = state_id
    storage.new(new_city)
    new_city.save()
    storage.close()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def PUT_city(city_id):
    """ updates city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    update_content = request.get_json()
    if not request.is_json:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]

    for key, val in update_content.items():
        if key not in ignore_keys:
            setattr(city, key, val)
    city.save()
    storage.close()
    return jsonify(city.to_dict()), 200
