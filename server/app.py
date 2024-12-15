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

            return make_response(new_user.to_dict(), 201)

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

                return make_response(user.to_dict(), 200)

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

                return make_response({}, 204)

         # handles any other type of exceptions
        except Exception as e:
            handle_exception(e)

class TrailsIndex(Resource):
    def post(self):
        try:
            address = request.json.get('city')
            trails = [trail.to_dict() for trail in Trail.query.all() if address.lower() in trail.address.lower()]

            # List of checks
            checks_list = [check_if_attribute(address), check_if_trail(trails)]

            error_message = None

            # loops through list and breaks if any of the checks have a value
            for check in checks_list:
                error_message = check
                if error_message:
                    break

            # Early return if there is an error
            if error_message:
                return error_message

            if trails:
                return make_response(trails, 201)

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
                return make_response(trail.to_dict(), 200)

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

    def put(self):
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

                db.session.commit()

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

    def put(self):
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
                
                db.session.commit()

                return make_response({}, 201)

        # Handle Exception
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)       

class ChangeUserRole(Resource):
    def post(self):
        inputed_admin_secret_key = request.json.get("adminSecretKey")
        app_admin_secret_key = app.admin_secret_key
        user_id = session["user_id"]
        user = User.query.filter(User.id == user_id).first()

        # Check if input_admin_secret_key has a value
        if not inputed_admin_secret_key:
            print("Inside no inputed admin secret key")
            return make_response(jsonify({"error" : "No data was recieved."}), 422)

        # Check if app_admin_secret_key has a value
        if not app_admin_secret_key:
            print("Inside no app admin secret key")
            return make_response(jsonify({"error" : "No app admin key found."}), 422)

        # Check if user_id has a value
        if not user_id:
            print("Inside no user id")
            return make_response(jsonify({"error" : "No user id was found."}), 422)

        # Check if user has a value
        if not user:
            print("inside no user")
            return make_response(jsonify({"error" : "Could not find a user with user id"}), 422)

        # Check if inputed key is same as app key
        if inputed_admin_secret_key == app_admin_secret_key:
            # Assign user role to admin
            user.role = "admin"

            db.session.commit()

            print("Inside input key is same as app key")
            return make_response(jsonify({"user role" : user.role}), 201)

        else:
            print(f"inputed key: {inputed_admin_secret_key}")
            print(f"app key: {app.admin_secret_key}")
            print("Inputed secret key does not match app secret key")
            return make_response(jsonify({"error" : "Invalid secret key"}), 422)

class CreateTrail(Resource):
    def post(self):
        try:
            data = request.get_json()
            trail_name = data.get("trailName", None)
            trail_address = data.get("trailAddress", None)
            trail_length = float(data['trailLength'])
            trail_description = data['trailDescription']
            trail_image_url = data['trailImageUrl']

            # Check if data has a value
            if not data:
                print("Inside no data was sent")
                return make_response(jsonify({"error" : "No data was recieved."}), 422)

            # Check if nay of the trial attributes do not have a value
            for attribute in [trail_name, trail_address, trail_length, trail_description, trail_image_url]:
                if not attribute:
                    print(f"attribute {attribute} has no value")
                    return make_response(jsonify({"error" : "Some attribute had no value"}), 422)

            new_trail = Trail(
                name=trail_name,
                address=trail_address,
                length=trail_length,
                description=trail_description,
                image_url=trail_image_url
            )

            # Check if new trail has any value
            if not new_trail:
                print("Inside new trail has no value")
                return make_response(jsonify({"error" : "New trail has no value."}), 422)

            # add new_review to session
            db.session.add(new_trail)
            db.session.commit()

            return make_response(new_trail.to_dict(), 201)

        # Handle Exception
        except Exception as e:
            db.session.rollback()
            print("inside xception")
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)  


class CheckPassword(Resource):
    def post(self):
        user_id = session['user_id']
        password = request.json.get('confirmationPassword')
        user = User.query.filter(User.id == user_id).first()

        # Check if password request data has a value
        if not password:
            print("inside no password")
            return make_response(jsonify({"error" : "No data received"}), 422)

        # Check if user_id has a value
        if not user_id:
            print("Inside no user id")
            return make_response(jsonify({"error" : "No user id was found."}), 422)

        # Check if user has a value
        if not user:
            print("inside no user")
            return make_response(jsonify({"error" : "Could not find a user with user id"}), 422)

        if user.authenticate(password):
            print("inside successful code")
            return make_response(jsonify({"message" : "password verified successfully!"}), 200)

        else:
            return make_response(jsonify({"error" : "inputed password does not match password in our system!"}), 422)


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

            # Check if user_id has a value
            if not user_id:
                print("Inside no user id")
                return make_response(jsonify({"error" : "No user id was found."}), 422)

            # Check if user has a value
            if not user:
                print("inside no user")
                return make_response(jsonify({"error" : "Could not find a user with user id"}), 422)

            # Check if request data was received
            if not data:
                print("inside no data")
                return make_response(jsonify({"error" : "No data was received"}), 422)

            # Check that the new username/password are not empty strings
            if not len(new_username) > 0 or not len(new_password) > 0:
                print("inside username or password empty")
                return make_response(jsonify({"error" : "Username or password cannot be empty"}), 400)

            # Assign new values to user object
            print(f"before: {user}")
            user.username = new_username
            user.password_hash = new_password
            user.profile_image_url = new_profile_image_url
            user.bio = new_bio
            print(f"after: {user}")

            db.session.commit()

            return make_response(jsonify({"message" : "User successfully updated!"}), 200)

        # Model column constraints errors
        except IntegrityError:
            db.session.rollback()
            print("IntegrityError: User Already exists.")
            return make_response(jsonify({'errors': 'Username already taken.'}), 422)

        # Any other exception
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'errors': f"{str(e)}"}), 422)

    def delete(self):
        try:
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            
            # Check if user_id has a value
            if not user_id:
                print("Inside no user id")
                return make_response(jsonify({"error" : "No user id was found."}), 422)

            # Check if user has a value
            if not user:
                print("inside no user")
                return make_response(jsonify({"error" : "Could not find a user with user id"}), 422)

            # Delete user from db
            db.session.delete(user)
            db.session.commit()

            # Remove user_id from sessoin
            session['user_id'] = None

            return make_response({}, 204)

        # Any other exception
        except Exception as e:
            db.session.rollback()
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
api.add_resource(ChangeUserRole, "/change_user_role", endpoint="change_user_role")
api.add_resource(CreateTrail, "/create_trail", endpoint="create_trail")
api.add_resource(CheckPassword, "/check_password", endpoint="check_password")
api.add_resource(EditUser, "/edit_user", endpoint="edit_user")


if __name__ == '__main__':
    app.run(port=5555, debug=True)

