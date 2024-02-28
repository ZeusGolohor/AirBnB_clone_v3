#!/usr/bin/python3
"""
A script to handle the City model
"""
from flask import jsonify, abort, request
from api.v1.views import place_views
from models import storage
from models.city import City
from models.place import Place


@place_views.route(
        "/places/<place_id>",
        strict_slashes=False,
        methods=["GET", "DELETE", "PUT"])
@place_views.route(
    "/cities/<city_id>/places",
    methods=["GET", "POST"],
    strict_slashes=False)
def all_cites(city_id=None, place_id=None):
    """
    A method to retrieve all states.
    """
    # setting the model for this method
    cls = Place
    cls1 = City
    # check if the request is a GET request.
    if (request.method == "GET"):
        # check if state_id is present
        if (place_id is not None):
            res = storage.all(cls)
            for key, value in res.items():
                if value.id == place_id:
                    return (jsonify(value.to_dict()))
        # check if the request is for a single
        # or multiple instance(s)
        elif (city_id is not None):
            places = []
            res = storage.all(cls1)
            for key, value in res.items():
                if (value.id == city_id):
                    res2 = storage.all(cls)
                    for key2, value2 in res2.items():
                        if value2.city_id == city_id:
                            places.append(value2.to_dict())
                    return (jsonify(places))
        # if no match is found return 404
        return (abort(404))

    # check if the request is to delete an instance
    # to delete an instance
    elif (request.method == "DELETE"):
        # check if the id exists
        if (place_id is not None):
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == place_id):
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
                data["city_id"]
                data["user_id"]
                data["name"]
                data["description"]
                data["number_rooms"]
                data["number_bathrooms"]
                data["max_guest"]
                data["price_by_night"]
                data["latitude"]
                data["longitude"]
                # check if the state exists
                city = []
                all_cities = storage.all(cls1)
                for key, value in all_cities.items():
                    if (value.id == city_id):
                        city = value
                if (city is None):
                    return (abort(404))
                data["city_id"] = city.id
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
            awd_keys = [
                "city_id",
                "user_id",
                "name",
                "description",
                "number_rooms",
                "number_bathrooms",
                "max_guest",
                "price_by_night",
                "latitude",
                "longitude"]
            res = storage.all(cls)
            for key, value in res.items():
                if (value.id == place_id):
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
