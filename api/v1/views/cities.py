#!/usr/bin/python3
"""
A script to handle the City model
"""
from flask import jsonify, abort, request
from api.v1.views import city_views
from models import storage
from models.city import City
from models.state import State

# @state_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
# @state_views.route("/cities", methods=["GET", "POST"], strict_slashes=False)
@city_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET", "DELETE", "PUT"])
@city_views.route("/states/<state_id>/cities", methods=["GET", "POST"], strict_slashes=False)
def all_cites(city_id=None, state_id=None):
    """
    A method to retrieve all states.
    """
    # setting the model for this method
    cls = City
    cls1 = State
    # check if the request is a GET request.
    if (request.method == "GET"):
        # check if state_id is present
        if (state_id is not None):
            cities = []
            res = storage.all(cls1)
            for key, value in res.items():
                if (value.id == state_id):
                    res2 = storage.all(cls)
                    for key, value in res2.items():
                        if (value.state_id == state_id):
                            cities.append(value.to_dict())
                    return (jsonify(cities))
        # check if the request is for a single
        # or multiple instance(s)
        elif (city_id is not None):
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == city_id):
                    return (jsonify(value.to_dict()))
        # if no match is found return 404
        return (abort(404))

    # check if the request is to delete an instance
    # to delete an instance
    elif (request.method == "DELETE"):
        # check if the id exists
        if (city_id is not None):
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == city_id):
                    value.delete()
                    storage.save()
                    return (jsonify({}), 200)
            return (abort(404))
    # check if the request is a post request
    # to create new instance(s)
    elif (request.method == "POST"):
        data = {}
        try:
            data = request.get_json()
            try:
                data["name"]
                # check if the state exists
                state = None
                all_state = storage.all(cls1)
                for key, value in all_state.items():
                    if (value.id == state_id):
                        state = value
                if (state == None):
                    return (abort(404))
                data["state_id"] = state.id
                ins = cls(**data)
                ins.save()
                return (ins.to_dict(), 201)
            except Exception as e:
                print(e)
                return (jsonify({"message": "Missing name"}), 400)
        except Exception as e:
            print(e)
            return (jsonify({"message": "Not a JSON"}), 400)
    elif (request.method == "PUT"):
        if (id is not None):
            awd_keys = ["name"]
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == city_id):
                    try:
                        data = request.get_json()
                        for key, value2 in data.items():
                            if (key in awd_keys):
                                setattr(value, key, value2)
                        value.save()
                        return (jsonify(value.to_dict()), 200)

                    except Exception as e:
                        print(e)
                        return jsonify({"message": "Not a JSON"}), 400

        return (abort(404))
          
