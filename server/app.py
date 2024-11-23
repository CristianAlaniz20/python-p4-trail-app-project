#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Trail, UserTrail, Review

# Views go here!

class Signup(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        username = data.get('username', None)
        password = data['password']
        image_url = data['profileImage']
        bio = data['bio']

        if not username:
            print("NO username in data!")#
            return make_response(jsonify({'errors': 'Missing username.'}), 422)

        new_user = User(username=username, profile_image_url=image_url, bio=bio)
        print(new_user)
        try:
            new_user.password_hash = password 

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            return make_response(new_user.to_dict(), 201)

        except IntegrityError:
            db.session.rollback()
            print("IntegrityError: User Already exists.")
            return make_response(jsonify({'errors': 'Username already taken.'}), 422)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

class Login(Resource):
    def post(self):
        # Get request information
        data = request.get_json()
        print(data)
        username = data.get('username', None)
        password = data['password']

        # Check if a user in db matches username in request
        user = User.query.filter(User.username == username).first()
        print(user)
        if not user:
            return make_response(jsonify({"error" : "invalid username"}), 401)

        # Check if password in request matches the password in db for User
        if user.authenticate(password):
            session['user_id'] = user.id

            return make_response(user.to_dict(), 200)

        # invalid username or password message
        return make_response(jsonify({"error" : "invalid username or password."}), 401)

class CheckSession(Resource):
    def get(self):
        user_id = session['user_id']
        print(f"user id: {user_id}")

        #check if user_id has any value
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return make_response(user.to_dict(), 200)
        else:
            return make_response(jsonify({"error" : "You are not logged in."}), 401)

class Logout(Resource):
    def delete(self):
        user_id = session['user_id']
        if user_id:
            session['user_id'] = None

            return make_response({}, 204)
        else:
            return make_response(jsonify({"error" : 'Cannot logout because you are already logged out'}), 401)


api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

