#!/usr/bin/python3
"""
New view for Amenity objects that handles all default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models import storage

@app_views.route('/states/<state_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def ALL_Amenities():
    """Retrieves the list of all Amenity objects"""
    retval = []
    all_amenities = storage.all('Amenity')
    for amenities in all_amenities.values():
        retval.append(amenities.to_dict())
    return jsonify(retval)

@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def GET_Amenity(amenity_id):
    """GET Amenity object, if amenity_id not linked - raise 404 """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def DEL_Amenity(amenity_id):
    """DELETE amenity, raise 404 on error, returns 200 on success"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def POST_Amenity(amenity_id):
    """Adds amenity, raise 400 upon error, returns 201 on success"""
    post_amenity = request.get_json()

    if not request.is_json:
        abort(400, "Not a JSON")

    name = post_amenity.get('name')
    if not name:
        abort(400, "Missing name")

    new_amenity = Amenity(**post_amenity)
    storage.new(new_amenity)

    new_amenity.save()
    storage.close()
    return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUTS'],
                 strict_slashes=False)
def PUT_Amenity(amenity_id):
    """Update amenity, raise 404 on error, 200 on success"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]

    amenity_info = request.get_json()

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, val in amenity_info.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)

    amenity.save()
    storage.close()

    return jsonify(amenity.to_dict()), 200
