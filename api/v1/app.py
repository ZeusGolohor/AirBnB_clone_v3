#!/usr/bin/python3
"""
A script for initializing flasks and
registering blueprints.
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception=None):
    # This function will be called when the application context ends
    if storage:
        storage.close()
        # print("Storage closed.")


@app.errorhandler(404)
def page_not_found(error):
    """
    A method to handle instances when resources are
    found.
    """
    # print(error)
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True, debug=True)