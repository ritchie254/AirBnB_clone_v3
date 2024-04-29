#!/usr/bin/python3
"""
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """
    retrieves city based on state id
    """
    allCities = []
    obj = storage.get("State", str(state_id))

    if obj is None:
        abort(404)
    for city in obj.cities:
        allCities.append(city.to_dict())

    return jsonify(allCities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def allCities(city_id):
    """
    retrieves city by id
    """
    obj = storage.get("City", str(city_id))

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def city_post(state_id):
    """
    post request for cities
    """
    obj = request.get_json(silent=True)
    if obj is None:
        abort(404, "Not a JSON")

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in obj:
        abort(404, "Missing name")

    obj["state_id"] = state_id
    newCity = City(**obj)
    newCity.save()

    return jsonify(newCity.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def put_city(city_id):
    """
    put request
    """
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")

    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in obj.items():
        if key not in ["id", "created_at", "state_id"]:
            setattr(fetched_obj, key, val)

    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"], strict_slashes=False)
def del_city(city_id):
    """
    delete request
    """
    obj = storage.get("City", str(city_id))

    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({})
