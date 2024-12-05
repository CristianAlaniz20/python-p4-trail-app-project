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
            if user:
                return make_response(user.to_dict(), 200)
            else:
                session['user_id'] = None
                return make_response(jsonify({"error": "User not found."}), 404)
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
            db.session.flush()
            print("new review added to session")
            new_review._username = new_review.user.username
           
            db.session.commit()
            print(f"new review: {new_review}")
            print(f"new review user: {new_review.user}")
            print(f"new review user username: {new_review.user.username}")

            return make_response(new_review.to_dict(), 201)
         
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

class SavedTrailsbyUserId(Resource):
    def get(self):
        try:
             # Get and Check user_id from the session
            user_id = session['user_id']
            if not user_id:
                return make_response(jsonify({"error" : "No user in session."}), 422)
            
            # Query database to get all saved trails for User
            saved_trails = (
                db.session.query(Trail)
                .join(UserTrail)
                .filter(UserTrail.user_id == user_id, UserTrail.is_saved == True)
                .all()
            )
            if not saved_trails:
                return make_response(jsonify({"error" : "No saved trails found."}), 200)

            # Serialize all trails in saved_trails
            serialized_saved_trails = [saved_trail.to_dict() for saved_trail in saved_trails]

            return make_response(serialized_saved_trails, 200)

        # Handle Exception
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

    def post(self):
        try:
            # Get and Check trail_id from the request
            request_trail_id = request.json.get("id")
            if not request_trail_id:
                print("Inside no request trail id")
                return make_response(jsonify({"error" : "Could not access request data"}), 422)

            # Get and Check user_id from the session
            session_user_id = session['user_id']
            if not session_user_id:
                print("Inside no session user id")
                return make_response(jsonify({"error" : "No user in session."}), 422)

            # Query UserTrail table to see if instance already exists
            user_trail = UserTrail.query.filter(UserTrail.user_id == session_user_id, UserTrail.trail_id == request_trail_id).first()

            # Create UserTrail instance 
            if not user_trail:
                print("Inside no user trail in db")
                newUserTrail = UserTrail(
                    user_id=session_user_id,
                    trail_id=request_trail_id
                )
                newUserTrail.is_saved = True

                # Check if UserTrail instance was created
                if not newUserTrail:
                    print("Inside no UserTrail instance created")
                    return make_response(jsonify({"error" : "Could not create UserTrail instance"}), 422)
            
                db.session.add(newUserTrail)
                db.session.commit()

                return make_response({}, 201)

            # Set the existinng instance is_saved value to True
            else:
                user_trail.is_saved = True

                return make_response({}, 201)

        # Handle Exception
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)  

class HikedTrailsbyUserId(Resource):
    def get(self):
        try:
             # Get and Check user_id from the session
            user_id = session['user_id']
            if not user_id:
                return make_response(jsonify({"error" : "No user in session."}), 422)
            
            # Query database to get all saved trails for User
            hiked_trails = (
                db.session.query(Trail)
                .join(UserTrail)
                .filter(UserTrail.user_id == user_id, UserTrail.is_hiked == True)
                .all()
            )
            if not hiked_trails:
                return make_response(jsonify({"error" : "No saved trails found."}), 200)

            # Serialize all trails in saved_trails
            serialized_hiked_trails = [hiked_trail.to_dict() for hiked_trail in hiked_trails]

            return make_response(serialized_hiked_trails, 200)

        # Handle Exception
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

    def post(self):
        try:
            # Get and Check trail_id from the request
            request_trail_id = request.json.get("id")
            if not request_trail_id:
                print("Inside no request trail id")
                return make_response(jsonify({"error" : "Could not access request data"}), 422)

            # Get and Check user_id from the session
            session_user_id = session['user_id']
            if not session_user_id:
                print("Inside no session user id")
                return make_response(jsonify({"error" : "No user in session."}), 422)

            # Query UserTrail table to see if instance already exists
            user_trail = UserTrail.query.filter(UserTrail.user_id == session_user_id, UserTrail.trail_id == request_trail_id).first()

            # Create UserTrail instance 
            if not user_trail:
                print("Inside no user trail in db")
                newUserTrail = UserTrail(
                    user_id=session_user_id,
                    trail_id=request_trail_id
                )
                newUserTrail.is_hiked = True

                # Check if UserTrail instance was created
                if not newUserTrail:
                    print("Inside no UserTrail instance created")
                    return make_response(jsonify({"error" : "Could not create UserTrail instance"}), 422)
            
                db.session.add(newUserTrail)
                db.session.commit()

                return make_response({}, 201)

            # Set the existinng instance is_saved value to True
            else:
                user_trail.is_hiked = True

                return make_response({}, 201)

        # Handle Exception
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
api.add_resource(SavedTrailsbyUserId, '/saved_trails', endpoint='saved_trails')
api.add_resource(HikedTrailsbyUserId, '/hiked_trails', endpoint='hiked_trails')



if __name__ == '__main__':
    app.run(port=5555, debug=True)

