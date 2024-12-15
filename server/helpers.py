# helper functions for app.py file

from flask import session, jsonify, make_response
from config import db

# checks if the request body has a value
def check_if_data(data):
    if not data:
        return make_response(jsonify({"error" : "No data was received!"}), 400)

# checks if the user_id has any value
def check_if_user_id(user_id):
    if not user_id:
        return make_response(jsonify({"error" : "No user id in the session."}), 401)

# checks if a user variable has any value
def check_if_user(user):
    if not user:
        return make_response(jsonify({"error" : "No user found."}), 404)

# checks if a trail_id has a value
def check_if_trail_id(trail_id):
    if not trail_id:
        return make_response(jsonify({"error" : "No trail id received."}), 400)

# checks if a trail has any value
def check_if_trail(trail):
    if not trail:
        return make_response(jsonify({"error" : "No trail found."}), 404)

# checks if an attribute has any value
def check_if_attribute(attribute):
    if len(attribute) == 0:
        return make_response(jsonify({"error" : "Input(s) cannot be empty."}), 400)

# checks if new_instance has value
def check_if_new_instance(new_instance):
    if not new_instance:
        return make_response(jsonify({"error" : "Could not create new record."}), 400)

# integrity error response
def handle_integrity_error():
    db.session.rollback()
    return make_response(jsonify({'error': 'Integrity Error: Does not follow constraint limitations.'}), 422)

# exception response
def handle_exception(exception):
    db.session.rollback()
    return make_response(jsonify({'error': f"{str(e)}"}), 500)

def duplicate_username():
    return make_response(jsonify({"error" : "User with that username already exists."}), 400)