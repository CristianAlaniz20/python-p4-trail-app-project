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
# Helper functions imports
from helpers import check_if_data, check_if_user_id, check_if_user, check_if_trail_id, check_if_trail, check_if_attribute, check_if_new_instance, handle_integrity_error, handle_exception, duplicate_username

# Views go here!

class Signup(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username', None)
            password = data['password']
            image_url = data['profileImage']
            bio = data['bio']

            # List of checks
            checks_list = [check_if_data(data), check_if_attribute(username), check_if_attribute(password)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Check if a user with the username already exists
            if User.query.filter(User.username == username).first():
                return duplicate_username()

            # create new user instance
            new_user = User(username=username, profile_image_url=image_url, bio=bio)
            
            # check if instance was created
            error_message = check_if_new_instance(new_user)

            if error_message:
                return error_message
        
            # assign password to instance
            new_user.password_hash = password 

            # add and commit to db
            db.session.add(new_user)
            db.session.commit()

            # assign new_user db instance id to session user_id
            session['user_id'] = new_user.id

            response = {
                "message" : "Sucessfully signed up!",
                "expected_data" : user.to_dict()
            }

            return make_response(jsonify(response), 201)

        # handles new instance does not respect model constraints
        except IntegrityError:
            handle_integrity_error()

        # handles any other type of exceptions
        except Exception as e:
            handle_exception(e)

class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username', None)
            password = data['password']
            user = User.query.filter(User.username == username).first()

            # List of checks
            checks_list = [check_if_data(data), check_if_attribute(username), check_if_attribute(password), check_if_user(user)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Check if password in request matches the password in db for User
            if user.authenticate(password):
                session['user_id'] = user.id

                response = {
                    "message" : "Sucessfully logged in!",
                    "expected_data" : user.to_dict()
                }

                return make_response(jsonify(response), 200)

            # invalid username or password message
            return make_response(jsonify({"error" : "invalid username or password."}), 401)
        
        # handles any other type of exceptions
        except Exception as e:
            handle_exception(e)

class CheckSession(Resource):
    def get(self):
        try:
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()

            # List of checks
            checks_list = [check_if_user_id(user_id), check_if_user(user)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            #check if user has any value
            if user:
                return make_response(user.to_dict(), 200)
            else:
                session['user_id'] = None
        
            return make_response(jsonify({"error" : "You are not logged in."}), 401)
        
        # handles any other type of exceptions
        except Exception as e:
            handle_exception(e)

class Logout(Resource):
    def delete(self):
        try:
            user_id = session['user_id']

            # check if user_id has a value 
            error_message = check_if_user_id(user_id)

            # Early return if there is an error
            if error_message:
                return error_message

            if user_id:
                session['user_id'] = None

                response = {"message" : "Successfully logged out!"}

                return make_response(jsonify(response), 200)

         # handles any other type of exceptions
        except Exception as e:
            handle_exception(e)

class TrailsIndex(Resource):
    def post(self):
        try:
            address = request.json.get('city')
            trails = [trail.to_dict() for trail in Trail.query.all() if address.lower() in trail.address.lower()]

            # Check if address has value
            error_message = check_if_attribute(address)

            if error_message:
                return error_message
            
            # frontend handles if trails has no value
            response = {
                "message" : "City received!",
                "expected_data" : trails
            }

            return make_response(jsonify(response), 201)

        except Exception as e:
            handle_exception(e)

class TrailById(Resource):
    def get(self, trail_id):
        try:
            trail = Trail.query.filter(Trail.id == trail_id).first()

            # List of checks
            checks_list = [check_if_trail_id(trail_id), check_if_trail(trail)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            if trail:
                response = {
                    "message" : "Trail found!",
                    "expected_data" : trail.to_dict()
                }

                return make_response(jsonify(response), 200)

        except Exception as e:
            handle_exception(e)

class ReviewsForTrail(Resource):
    def get(self, trail_id):
        try:
            reviews = [review.to_dict() for review in Review.query.all() if review.trail_id == trail_id]

            # Check if error_message has a value
            error_message = check_if_trail_id(trail_id)

            if error_message:
                return error_message

            # frontend handles if reviews is empty
            return make_response(reviews, 200)

        except Exception as e:
            handle_exception(e)

    def post(self, trail_id):
        try:
            user_id = session['user_id']
            data = request.get_json()
            rating = data['rating']
            text = data['text']

            # List of checks
            checks_list = [check_if_trail_id(trail_id), check_if_user_id(user_id), check_if_data(data)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # create new review instance
            new_review = Review(
                rating=rating,
                text=text
            )

            # check if instance was created
            error_message = check_if_new_instance(new_review)

            if error_message:
                return error_message

            # Assign the new reviews trail and user id's
            new_review.trail_id = trail_id
            new_review.user_id = user_id

            # add new review instance to db
            db.session.add(new_review)
            db.session.flush()
            
            # assign the new reviews _username attribute
            new_review._username = new_review.user.username
           
            # commit to db
            db.session.commit()

            response = {
                "message" : "Review sucessfully created!",
                "expected_data" : new_review.to_dict()
            }

            return make_response(jsonify(response), 201)
         
        except Exception as e:
            handle_exception(e)

class SavedTrailsbyUserId(Resource):
    def get(self):
        try:
            user_id = session['user_id']
            
            # check if error_message has a value
            error_message = check_if_user_id(user_id)

            if error_message:
                return error_message
            
            # Query database to get all saved trails for User
            saved_trails = (
                db.session.query(Trail)
                .join(UserTrail)
                .filter(UserTrail.user_id == user_id, UserTrail.is_saved == True)
                .all()
            )

            # Serialize all trails in saved_trails
            serialized_saved_trails = [saved_trail.to_dict() for saved_trail in saved_trails]

            return make_response(serialized_saved_trails, 200)

        # Handle Exception
        except Exception as e:
            handle_exception(e)

    def post(self):
        try:
            request_trail_id = request.json.get("id")
            session_user_id = session['user_id']
            
            # List of checks
            checks_list = [check_if_trail_id(request_trail_id), check_if_user_id(session_user_id)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Query UserTrail table to see if instance already exists
            user_trail = UserTrail.query.filter(UserTrail.user_id == session_user_id, UserTrail.trail_id == request_trail_id).first()

            # Create UserTrail instance 
            if not user_trail:
                newUserTrail = UserTrail(
                    user_id=session_user_id,
                    trail_id=request_trail_id
                )
                newUserTrail.is_saved = True

                # Check if UserTrail instance was created
                error_message = check_if_new_instance(newUserTrail)
                
                if error_message:
                    return error_message
            
                # add and commit new UserTrail instance to db
                db.session.add(newUserTrail)
                db.session.commit()

                return make_response(jsonify({"message" : "Trail has been saved and recorded."}), 201)

            # Set the existinng instance is_saved value to True
            else:
                user_trail.is_saved = True

                db.session.commit()

                return make_response(jsonify({"message" : "Trail has been saved."}), 201)

        # Handle Exception
        except Exception as e:
            handle_exception(e)  

class HikedTrailsbyUserId(Resource):
    def get(self):
        try:
             # Get and Check user_id from the session
            user_id = session['user_id']
            
            # check if error_message has a value
            error_message = check_if_user_id(user_id)

            if error_message:
                return error_message
            
            # Query database to get all saved trails for User
            hiked_trails = (
                db.session.query(Trail)
                .join(UserTrail)
                .filter(UserTrail.user_id == user_id, UserTrail.is_hiked == True)
                .all()
            )

            # Serialize all trails in saved_trails
            serialized_hiked_trails = [hiked_trail.to_dict() for hiked_trail in hiked_trails]

            # frontend handles if list is empty
            return make_response(serialized_hiked_trails, 200)

        # Handle Exception
        except Exception as e:
            handle_exception(e)

    def post(self):
        try:
            request_trail_id = request.json.get("id")
            session_user_id = session['user_id']
                
            # List of checks
            checks_list = [check_if_trail_id(request_trail_id), check_if_user_id(session_user_id)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Query UserTrail table to see if instance already exists
            user_trail = UserTrail.query.filter(UserTrail.user_id == session_user_id, UserTrail.trail_id == request_trail_id).first()

            # Create UserTrail instance 
            if not user_trail:
                newUserTrail = UserTrail(
                    user_id=session_user_id,
                    trail_id=request_trail_id
                )
                newUserTrail.is_hiked = True

                # Check if UserTrail instance was created
                error_message = check_if_new_instance(newUserTrail)
                    
                if error_message:
                    return error_message
                
                # add and commit new UserTrail instance to db
                db.session.add(newUserTrail)
                db.session.commit()

                return make_response(jsonify({"message" : "Trail is marked as hiked and recorded."}), 201)

            # Set the existinng instance is_hiked value to True
            else:
                user_trail.is_hiked = True
                    
                db.session.commit()

                return make_response(jsonify({"message" : "Trail is marked as hiked."}), 201)

        # Handle Exception
        except Exception as e:
            handle_exception(e)

class ChangeUserRole(Resource):
    def post(self):
        try:
            inputed_admin_secret_key = request.json.get("adminSecretKey")
            app_admin_secret_key = app.admin_secret_key
            user_id = session["user_id"]
            user = User.query.filter(User.id == user_id).first()

            # List of checks
            checks_list = [check_if_attribute(inputed_admin_secret_key), check_if_attribute(app_admin_secret_key), check_if_user_id(user_id), check_if_user(user)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Check if inputed key is same as app key
            if inputed_admin_secret_key == app_admin_secret_key:
                # Assign user role to admin
                user.role = "admin"

                db.session.commit()

                return make_response(jsonify({"message" : "Account role successfully changed to admin."}), 201)

            else:
                return make_response(jsonify({"error" : "Invalid secret key."}), 422)

        # Handle Exception
        except Exception as e:
            handle_exception(e)

class CreateTrail(Resource):
    def post(self):
        try:
            data = request.get_json()
            trail_name = data.get("trailName", None)
            trail_address = data.get("trailAddress", None)
            trail_length = float(data['trailLength'])
            trail_description = data['trailDescription']
            trail_image_url = data['trailImageUrl']

            # List of checks
            checks_list = [check_if_data(data), check_if_attribute(trail_name), check_if_attribute(trail_address), check_if_attribute(str(trail_length)), check_if_attribute(trail_description), check_if_attribute(trail_image_url)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # create a Trail model instance
            new_trail = Trail(
                name=trail_name,
                address=trail_address,
                length=trail_length,
                description=trail_description,
                image_url=trail_image_url
            )

            # Check if new trail has any value
            error_message = check_if_new_instance(new_trail)
            if error_message:
                return error_message

            # add new_review to session
            db.session.add(new_trail)
            db.session.commit()

            if new_trail:
                return make_response(new_trail.to_dict(), 201)
        
        # Handle Exception
        except Exception as e:
            handle_exception(e)

class CheckPassword(Resource):
    def post(self):
        try:
            user_id = session['user_id']
            password = request.json.get('confirmationPassword')
            user = User.query.filter(User.id == user_id).first()

            # List of checks
            checks_list = [check_if_user_id(user_id), check_if_attribute(password), check_if_user(user)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Check if password matches whats in db
            if user.authenticate(password):
                return make_response(jsonify({"message" : "password verified successfully!"}), 200)

            return make_response(jsonify({"error" : "Inputed password does not match password in the system."}), 401)

        # Handle Exception
        except Exception as e:
            handle_exception(e)

class EditUser(Resource):
    def put(self):
        try:
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            data = request.get_json()
            new_username = data['newUsername']
            new_password = data['newPassword']
            new_profile_image_url = data['newProfileImage']
            new_bio = data['newBio']

            # List of checks
            checks_list = [check_if_user_id(user_id), check_if_user(user), check_if_data(data), check_if_attribute(new_username), check_if_attribute(new_password)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Assign new values to user object
            user.username = new_username
            user.password_hash = new_password
            user.profile_image_url = new_profile_image_url
            user.bio = new_bio

            # Commit changed to db
            db.session.commit()

            return make_response(jsonify({"message" : "User successfully updated!"}), 200)

        # Model column constraints errors
        except IntegrityError:
            handle_integrity_error()

        # Any other exception
        except Exception as e:
            handle_exception(e)

    def delete(self):
        try:
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            
            # List of checks
            checks_list = [check_if_user_id(user_id), check_if_user(user)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            # Delete user from db
            db.session.delete(user)
            db.session.commit()

            # Remove user_id from session
            session['user_id'] = None

            return make_response(jsonify({"message" : "User successfully deleted."}), 200)

        # Any other exception
        except Exception as e:
            handle_exception(e)

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TrailsIndex, '/trails_index', endpoint='trails_index')
api.add_resource(TrailById, '/trail/<int:trail_id>', endpoint='trail_by_id')
api.add_resource(ReviewsForTrail, '/reviews/<int:trail_id>', endpoint='reviews')
api.add_resource(SavedTrailsbyUserId, '/saved_trails', endpoint='saved_trails')
api.add_resource(HikedTrailsbyUserId, '/hiked_trails', endpoint='hiked_trails')
api.add_resource(ChangeUserRole, "/change_user_role", endpoint="change_user_role")
api.add_resource(CreateTrail, "/create_trail", endpoint="create_trail")
api.add_resource(CheckPassword, "/check_password", endpoint="check_password")
api.add_resource(EditUser, "/edit_user", endpoint="edit_user")


if __name__ == '__main__':
    app.run(port=5555, debug=True)

