#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, abort
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403

app.register_blueprint(app_views)

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
