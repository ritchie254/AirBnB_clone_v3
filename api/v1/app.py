#!/usr/bin/python3

"""
flask app
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """
    close the storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """
    handle the 404 error page
    """
    txt = {"error": "Not found"}
    return make_response(jsonify(txt), 404)


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"), debug=True)
