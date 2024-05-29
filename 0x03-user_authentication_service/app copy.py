#!/usr/bin/env python3
"""
Flask application.

This application defines a REST API with routes to register, log in,
and log out users.

Usage:
    Run the application:
        python app.py

    Access the endpoints:
        - GET http://localhost:5000/
        - POST http://localhost:5000/users
        - POST http://localhost:5000/sessions
        - DELETE http://localhost:5000/sessions

    Payload:
        - For user registration (POST /users):
            Form data: 'email', 'password'
        - For user login (POST /sessions):
            Form data: 'email', 'password'
        - For user logout (DELETE /sessions):
            Cookie: 'session_id'

    Response:
        - For user registration:
            - 200 OK: User created successfully
                {"email": "<registered email>", "message": "user created"}
            - 400 BAD REQUEST: Email already registered
                {"message": "email already registered"}
        - For user login:
            - 200 OK: User logged in successfully
                {"email": "<user email>", "message": "logged in"}
            - 401 UNAUTHORIZED: Incorrect login information
        - For user logout:
            - 302 Found: User logged out and redirected to GET /
            - 403 FORBIDDEN: Invalid session ID
"""
from flask import Flask, jsonify, request, abort, make_response, \
    redirect, url_for
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


@app.route("/sessions", methods=["POST"])
def login():
    """
    Handle POST requests to log in a user.

    Returns:
        dict: A JSON response indicating success or failure.
    """
    email = request.form["email"]
    password = request.form["password"]
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    Handle DELETE requests to log out a user.

    Returns:
        A redirection to the root endpoint or a 403 status code.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
