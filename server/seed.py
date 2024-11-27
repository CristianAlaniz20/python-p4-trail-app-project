#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc, uniform

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Trail, UserTrail, Review

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        # Delete previous records
        print("deleting previous records...")
        User.query.delete()
        Trail.query.delete()
        UserTrail.query.delete()
        Review.query.delete()

        # Create User records
        print("creating records...")

        # make sure users have unique usernames
        users = []
        usernames = []

        for i in range(10):
            
            username = fake.first_name()
            while username in usernames:
                username = fake.first_name()
            usernames.append(username)

            user = User(
                username=username,
                bio=fake.paragraph(nb_sentences=3),
                profile_image_url=fake.url(),
            )

            user.password_hash = user.username + 'password'

            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        # Create Trail records
        print("creating Trails...")

        trails = []
        names = []

        for i in range(20):
            name = fake.name()
            while name in names:
                name = fake.name()
            names.append(name)

            trail = Trail(
                name=name,
                address=fake.address(),
                length=uniform(0.5, 10),
                description=fake.paragraph(nb_sentences=1),
                image_url=fake.url()
            )

            trails.append(trail)

        db.session.add_all(trails)
        db.session.commit()

        # Create UserTrail records
        print("Creating UserTrails...")  
        user_trails = []

        for i in range(15):
            user_trail = UserTrail(
                user = rc(users),
                trail = rc(trails)
            )

            user_trails.append(user_trail)

        db.session.add_all(user_trails)
        db.session.commit()

        # Create Review records
        print("Creating Reviews...")
        reviews = []

        for i in range(50):
            review = Review(
                rating=uniform(0, 5),
                text=fake.paragraph(nb_sentences=3),
                user = rc(users),
                trail = rc(trails)
            )
            db.session.add(review)
            db.session.flush()

            review._username = review.user.username

        db.session.commit()

        print("database seeded!")