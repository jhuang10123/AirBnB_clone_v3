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

# #Retrieves a State object: GET /api/v1/states/<state_id>
# @app.route('/states/<int:state_id>', methods=['GET'])
# #try except 404
