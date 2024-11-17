from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    
    pass

class Trail(db.Model, SerializerMixin):
    __tablename__ = "trails"

    pass

class UserTrail(db.Model, SerializerMixin):
    __tablename__ = "user_trails"

    pass

class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    pass