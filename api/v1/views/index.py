#!/usr/bin/python3
"""
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def success():
    """
    returns status of ok
    """
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def all_count():
    """
    count all the instances
    """
    data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(data)
