#!/usr/bin/python3
"""
A script used for routing.
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """
    A method used to check the application
    status.
    """    
    return jsonify({"status": "OK"})
