from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    # Create User Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    profile_image_url = db.Column(db.String)
    bio = db.Column(db.String)

    # Create model relationships
    user_trails = db.relationship("UserTrail", back_populates="user", cascade="all, delete-orphan")

    reviews = db.relationship('Review', back_populates="user", cascade='all, delete-orphan')

    # Assocation proxy to reach trails
    trails = association_proxy('user_trails', 'trail', creator=lambda trail_obj: UserTrail(trail=trail_obj))

    # Serialization rules
    serialize_rules = ('-user_trails', '-reviews',)

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

    # Create Trail columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    length = db.Column(db.Float)
    description = db.Column(db.String)
    image_url = db.Column(db.String)

    # Create model relationships
    user_trails = db.relationship("UserTrail", back_populates="trail", cascade="all, delete-orphan")

    reviews = db.relationship('Review', back_populates="trail", cascade='all, delete-orphan')

    # Assocation proxy to reach trails
    users = association_proxy('user_trails', 'user', creator=lambda user_obj: UserTrail(user=user_obj))

    # Serialization rules
    serialize_rules = ('-user_trails', '-reviews',)

    # For debugging purposes
    def __repr__(self):
      return f'Trail ID {self.id}, NAME {self.name}, LENGTH {self.length}, ADDRESS {self.address}, Image URL {self.image_url}, DESCRIPTION {self.description}'

    # Checks that description is not longer than 100 characters
    @validates('description')
    def validates_instructions(self, key, value):
        if len(value) > 100:
            raise ValueError("Description cannot be more than 100 characters long.")
        return value

    
class UserTrail(db.Model, SerializerMixin):
    __tablename__ = "user_trails"

    # Create UserTrail Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.id'))
    is_hiked = db.Column(db.Boolean, default=False, nullable=False)

    # Create model relationships
    user = db.relationship("User", back_populates="user_trails")

    trail = db.relationship("Trail", back_populates="user_trails")

    # For debugging purposes
    def __repr__(self):
      return f'UserTrail ID {self.id}, User_ID {self.user_id}, Trail_ID {self.trail_id}, Is_Hiked {self.is_hiked}'


class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    #Create Review Columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    trail_id = db.Column(db.Integer, db.ForeignKey('trails.id'))
    _username = db.Column(db.String)

    # Create model relationships
    user = db.relationship("User", back_populates="reviews")

    trail = db.relationship("Trail", back_populates="reviews")

    # Serialization rules
    serialize_rules = ('-user', '-trail',)

    # For debugging purposes
    def __repr__(self):
      return f'Review ID {self.id}, RATING {self.rating}, TEXT {self.text}, User_ID {self.user_id}, Trail_ID {self.trail_id}, USERNAME {self._username}'
