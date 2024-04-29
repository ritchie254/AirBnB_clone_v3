#!/usr/bin/python3

"""
"""
from flask import jsonify, request, abort
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all():
    """
    retrieves all the states
    """
    list_State = []
    all_States = storage.all("State")

    for obj in all_States.values():
        list_State.append(obj.to_dict())

    return jsonify(list_State)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_by_id(state_id):
    """
    retrieves state based on id provided
    """
    stateId = storage.get("State", str(state_id))

    if stateId is None:
        abort(404)
    return jsonify(stateId.to_dict())


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_to():
    """
    sends a post request to web
    """
    post_info = request.get_json(silent=True)

    if post_info is None:
        abort(400, "Not a JSON")
    if "name" not in post_info:
        abort(400, "Missing Name")

    newState = State(**post_info)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_value(state_id):
    """
    sends a put request to web
    used for updating vlaues
    """
    post_info = request.get_json(silent=True)
    if post_info is None:
        abort(400, "Not a JSON")

    Obj = storage.get("State", str(state_id))
    if Obj is None:
        abort(404)
    for key, value in post_info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(Obj, key, value)
    Obj.save()
    return jsonify(Obj.to_dict()), 200


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_obj(state_id):
    """
    deletes an object using its id
    """
    Obj = storage.get("State", str(state_id))

    if Obj is None:
        abort(404)

    storage.delete(Obj)
    storage.save()

    return jsonify({}), 200
