#!/usr/bin/python3
"""
A script used for routing.
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """
    A method used to check the application
    status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stat():
    """
    A method to get the statistics for all models
    from the specified storage system.
    """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage

    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review,
               "State": State, "User": User}

    stats = {}
    for key, cls in classes.items():
        stats[key] = storage.count(cls)
    return jsonify(stats)
