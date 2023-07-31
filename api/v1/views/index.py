#!/usr/bin/python3
'''
    flask with general routes
    routes:
        /status:    display "status":"OK"
        /stats:     display total for all classes
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    '''
    Return JSON with status "OK".

    Returns:
        JSON: {"status": "OK"}
    '''
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=['GET'])
def storage_counts():
    '''
    Return counts of all classes in storage.

    Returns:
        JSON: {
            "amenities": <count of amenities>,
            "cities": <count of cities>,
            "places": <count of places>,
            "reviews": <count of reviews>,
            "states": <count of states>,
            "users": <count of users>
        }
    '''
    cls_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(cls_counts)
