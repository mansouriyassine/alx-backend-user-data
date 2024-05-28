#!/usr/bin/env python3
"""
Flask application.
"""


from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    Handle GET requests on the root endpoint.

    Returns:
        dict: A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
