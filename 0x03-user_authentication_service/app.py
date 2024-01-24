#!/usr/bin/env python3
'''module for app.py'''

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def register_user():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
