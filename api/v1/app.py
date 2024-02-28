#!/usr/bin/python3
"""
A script for initializing flasks and
registering blueprints.
"""
from flask import Flask, jsonify, request
from api.v1.views import (
    app_views, state_views,
    city_views, amenity_views,
    user_views, place_views,
    review_views
    )
from models import storage
import os
from flask_cors import CORS


app = Flask(__name__)
#  Adding CORS to our application
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
# Route Registration for the application
app.register_blueprint(app_views)
app.register_blueprint(state_views)
app.register_blueprint(city_views)
app.register_blueprint(amenity_views)
app.register_blueprint(user_views)
app.register_blueprint(place_views)
app.register_blueprint(review_views)


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
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not found"}), 404
    else:
        return (error)


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True, debug=True)
