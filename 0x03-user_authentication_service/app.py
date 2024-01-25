#!/usr/bin/env python3
'''module for app.py'''

from flask import Flask, jsonify, request, abort, make_response
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
        response = make_response(jsonify({'email': email, 'message': 'logged in'}))
        response.set_cookie('session_id', session_id, path='/')

        return response
    else:
        abort(401, "Unauthorized")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
