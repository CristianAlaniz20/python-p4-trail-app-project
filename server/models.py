from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    # Create Model Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    profile_image_url = db.Column(db.String)
    bio = db.Column(db.String)

    # For debugging purposes
    def __repr__(self):
      return f'User {self.username}, ID {self.id}, Image URL {self.profile_image_url}, BIO {self.bio}'

    # Hashing and Salting password
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes are not accessible.")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
        password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

class Trail(db.Model, SerializerMixin):
    __tablename__ = "trails"

    pass

class UserTrail(db.Model, SerializerMixin):
    __tablename__ = "user_trails"

    pass

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    pass