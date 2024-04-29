#!/usr/bin/python3

"""
"""
from flask import jsonify, request, abort
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_user():
    """
    gets all the users
    """
    allusers = []
    fetched = storage.all("User")

    for user in fetched.values():
        allusers.append(user.to_dict())

    return jsonify(allusers)


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def get_userById(user_id):
    """
    get request to ferch user based on ita id
    """
    obj = storage.get("User", str(user_id))

    if obj is None:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """
    post request
    """
    obj = request.get_json(silent=True)

    if obj is None:
        abort(400, "Not a JSON")
    if "email" not in obj:
        abort(400, "Missing email")
    if "password" not in obj:
        abort(400, "Missing password")

    all_obj = User(**obj)
    all_obj.save()

    return jsonify(all_obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_users(user_id):
    """
    put request
    """
    obj = request.get_json(silent=True)
    if obj is None:
        abort(400, "Not a JSON")

    fetched = storage.get("User", str(user_id))
    if fetched is None:
        abort(404)
    for key, val in obj.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched, key, val)

    fetched.save()
    return jsonify(fetched.to_dict())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def delete_users(user_id):
    """
    delete request
    """
    obj = storage.get("User", str(user_id))

    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return jsonify({})
