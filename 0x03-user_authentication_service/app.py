#!/usr/bin/env python3
"""
Flask application.

This application defines a REST API with a single POST route to register users.

Usage:
    Run the application:
        python app.py

    Access the endpoint:
        POST http://localhost:5000/users

    Payload:
        Form data: 'email', 'password'

    Response:
        - 200 OK: User created successfully
            {"email": "<registered email>", "message": "user created"}
        - 400 BAD REQUEST: Email already registered
            {"message": "email already registered"}

"""


from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    """
    Handle GET requests on the root endpoint.

    Returns:
        dict: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Handle POST requests to register a user.

    Returns:
        dict: A JSON response indicating success or failure.
    """
    try:
        email = request.form["email"]
        password = request.form["password"]
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
