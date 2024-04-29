#!/usr/bin/python3

"""
"""
from flask import jsonify, request, abort
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenity():
    """
    gets all the amenties
    """
    allAmenities = []
    fetched = storage.all("Amenity")

    for amenity in fetched.values():
        allAmenities.append(amenity.to_dict())

    return jsonify(allAmenities)


@app_views.route("/amenities/<amenity_id>",  methods=["GET"], strict_slashes=False)
def get_amenityById(amenity_id):
    """
    get request to ferch amentiy based on ita id
    """
    obj = storage.get("Amenity", str(amenity_id))

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenities():
    """
    post request
    """
    obj = request.get_json(silent=True)

    if obj is None:
        abort(400, "Not a JSON")
    if "name" not in obj:
        abort(400, "Missing name")

    all_obj = Amenity(**obj)
    all_obj.save()

    return jsonify(all_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def put_amemities(amenity_id):
    """
    put request
    """
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")

    fetched = storage.get("Amenity", str(amenity_id))
    if fetched is None:
        abort(404)
    for key, val in obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched, key, val)

    fetched.save()
    return jsonify(fetched.to_dict())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"], strict_slashes=False)
def delete_amenities(amenity_id):
    """
    delete request
    """
    obj = storage.get("Amenity", str(amenity_id))

    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({})
