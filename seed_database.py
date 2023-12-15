import os
import crud
from random import  randint

import server
from flask import Flask

import model
os.system("dropdb tic")
os.system("createdb tic")

# Creating a Flask app to use in the context
model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()



    # Function to seed the database with some initial data
    def seed_database():
        # Add users
        for _ in range(5):
            email = f'user{_}@example.com'
            password = 'password'
            wins = randint(0, 10)
            losses = randint(0, 10)
            draws = randint(0, 10)

            user = crud.create_user(email, password, wins, losses, draws)
            model.db.session.add(user)

        # Commit the changes to the database
        model.db.session.commit()


    seed_database()
    print('Database seeded successfully!')