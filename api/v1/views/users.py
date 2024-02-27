#!/usr/bin/python3
"""
A script to handle the Amenity model
"""
from flask import jsonify, abort, request
from api.v1.views import user_views
from models import storage
from models.user import User

@user_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"], strict_slashes=False)
@user_views.route("/users", methods=["GET", "POST"], strict_slashes=False)
def all_states(user_id=None):
    """
    A method to retrieve all states.
    """
    # setting the model for this method
    cls = User
    id = user_id
    # check if the request is a GET request.
    if (request.method == "GET"):
        # check if the request is for a single
        # or multiple instance(s)
        if (id is None):
            # store instance(s)
            ins = []
            # get all instance(s)
            res = storage.all(cls)
            for key, value in res.items():
                ins.append(value.to_dict())
            return (jsonify(ins))
        else:
            # get single instance(s)
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == id):
                    return (jsonify(value.to_dict()))

            return (abort(404))
    # check if the request is to delete an instance
    # to delete an instance
    elif (request.method == "DELETE"):
        # check if the id exists
        if (id is not None):
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == id):
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
                ins = cls(**data)
                ins.save()
                return (ins.to_dict(), 201)
            except Exception:
                return (jsonify({"message": "Missing name"}), 400)
        except Exception:
            return (jsonify({"message": "Not a JSON"}), 400)
    elif (request.method == "PUT"):
        if (id is not None):
            awd_keys = ["name"]
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == id):
                    try:
                        data = request.get_json()
                        for key, value2 in data.items():
                            if (key in awd_keys):
                                setattr(value, key, value2)
                        value.save()
                        return (jsonify(value.to_dict()), 200)

                    except Exception:
                        return jsonify({"message": "Not a JSON"}), 400

        return (abort(404))
          
