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

class TrailsIndex(Resource):
    def post(self):
        address = request.json.get('city')

        if not address:
            print("no adress")
            return make_response(jsonify({"error" : "No city was received"}), 422)

        try:
            trails = [trail.to_dict() for trail in Trail.query.all() if address.lower() in trail.address.lower()]

            return make_response(trails, 201)

        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

        print("Something went wrong")
        return make_response(jsonify({"error" : "Something went wrong"}), 404)

class TrailById(Resource):
    def get(self, trail_id):
        if not trail_id:
            return make_response(jsonify({"error" : "No id is found."}), 422)

        try:
            trail = Trail.query.filter(Trail.id == trail_id).first()

            return make_response(trail.to_dict(), 200)

        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

class ReviewsForTrail(Resource):
    def get(self, trail_id):
        if not trail_id:
            print("no trail id")
            return make_response(jsonify({"error" : "No id is found."}), 422)

        try:
            reviews = [review.to_dict() for review in Review.query.all() if review.trail_id == trail_id]

            return make_response(reviews, 200)

        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

    def post(self, trail_id):
        user_id = session['user_id']

        # Check if trail_id and user_id have a value
        if not trail_id or not user_id:
            return make_response(jsonify({"error" : "Could not get trail_id or user_id"}), 422)

        data = request.get_json()
        rating = data['rating']
        text = data['text']

        # Check if ReviewForm information was recieved
        if not data:
            return make_response(jsonify({"error" : "No data was received."}), 422)

        try:
            new_review = Review(
                rating=rating,
                text=text
            )
            new_review.trail_id = trail_id
            new_review.user_id = user_id

            db.session.add(new_review)
            db.session.commit()
            print(new_review)
        
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)
            



api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TrailsIndex, '/trails_index', endpoint='trails_index')
api.add_resource(TrailById, '/trail/<int:trail_id>', endpoint='trail_by_id')
api.add_resource(ReviewsForTrail, '/reviews/<int:trail_id>', endpoint='reviews')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

