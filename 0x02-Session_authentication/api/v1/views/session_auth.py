#!/usr/bin/env python3
"""
SessionAuth module
"""
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST', 'GET'], strict_slashes=False)
def auth_session_login() -> str:
    """
    Authenticates a user based on email and password, and creates a session
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            return jsonify({"error": "email missing"}), 400

        if not password:
            return jsonify({"error": "password missing"}), 400

        user = User.search({'email': email})

        if not user:
            return jsonify({"error": "no user found for this email"}), 404

        if not user[0].is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        # Create a Session ID for the User ID
        session_id = auth.create_session(user[0].id)

        # Set the cookie to the response
        response = jsonify(user[0].to_json())
        response.set_cookie(auth.session_name, session_id)

        return response

    return jsonify({"message": "Method Not Allowed"}), 405
