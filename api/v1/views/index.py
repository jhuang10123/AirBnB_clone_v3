#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify 
from models import storage

@app_views.route('/status')
def status():
    """return status in json format"""
    s = {"status": "OK"}
    return jsonify(s)

@app_views.route('/stats')
def stats():
    """ """
    classes = {"amenities": "Amenity", "cities": "City", 
               "places": "Place", "reviews": "Review",
               "states": "State", "users": "User"}
    retval = {}
    for key, val in classes.items():
        retval[key] = storage.count(val)
        print(key, retval[key])
    return retval


# places 1
# cities 2
# users 2
# amenities 0
# states 2
# reviews 1
# TypeError: 'dict' object is not callable
