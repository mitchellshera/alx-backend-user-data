#!/usr/bin/env python3
'''module for app.py'''

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    '''welcome message'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    '''register user'''
    try:
        email = request.form['email']
        password = request.form['password']

        user = AUTH.register_user(email, password)

        response_data = {"email": user.email, "message": "user created"}
        status_code = 200
    except ValueError as e:
        response_data = {"message": str(e)}
        status_code = 400

    return jsonify(response_data), status_code


@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, "Missing email or password")

    if AUTH.valid_login(email, password):
        # Create a new session for the user
        session_id = AUTH.create_session(email)

        # Set session ID as a cookie in the response
        response = make_response(jsonify({
            'email': email, 'message': 'logged in'}))
        response.set_cookie('session_id', session_id, path='/')

        return response
    else:
        abort(401, "Unauthorized")


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Logout function to respond to the DELETE /sessions route.
    The request is expected to contain the session ID
    as a cookie with key "session_id".
    Find the user with the requested session ID. If the
    user exists, destroy the session
    and redirect the user to GET /. If the user does not
    exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        # No session ID provided
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        # User not found
        abort(403)

    # User found, destroy the session
    AUTH.destroy_session(user.id)

    # Redirect the user to GET /
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    '''profile function to respond to the GET /profile route.'''
    session_id = request.cookies.get('session_id')

    if not session_id:
        # No session ID provided
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        # User not found
        abort(403)

    # User found, respond with JSON payload
    response_data = {"email": user.email}
    return jsonify(response_data), 200

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''get_reset_password_token function to respond
    to the POST /reset_password route.'''
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError as e:
        abort(403, description=str(e))

    return jsonify({
        'email': email,
        'reset_token': reset_token
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
