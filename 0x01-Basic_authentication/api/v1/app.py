#!/usr/bin/env python3
"""
Main route module for the API
"""
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

auth = None

AUTH_TYPE = getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth as AuthType
    auth = AuthType()


def before_request():
    """
    Filter each request before it's handled by the proper route
    """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if request.path not in excluded_paths and \
            auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401, description="Unauthorized")
        if auth.current_user(request) is None:
            abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    Returns:
        JSON response with a 404 error message
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    Returns:
        JSON response with a 401 error message
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    Returns:
        JSON response with a 403 error message
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
