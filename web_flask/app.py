#! /usr/bin/env python3
"""This is flask app"""
import hashlib
import os
import sys

from flask import Flask, abort, jsonify, make_response, render_template, redirect, request, url_for
from models import storage
from models import storage_type
from models.system_user import Person
from models.user import User
from models.utils.support import get_current_lat_lon


app = Flask(__name__)

# define global variable
userN = 'user_name'
userT = 'user_type'

personN_err = {
    'first_name': 'Missing first_name',
    'last_name': 'Missing last_name',
    'email': 'Missing email',
    'gender': 'Missing gender',
    'phone_number': 'Missing phone_number'
}

# Home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    """Home page"""
    loc = get_current_lat_lon()
    # my_map = Map('my-map', center=[-41.139416, -73.025431], zoom=16)

    return (render_template('home.html'))

# Ambulance page
@app.route('/ambulance', methods=['GET'])
def ambulance():
    """Ambulance page"""
    return (render_template('ambu.html'))

# Hospital page
@app.route('/hospital', methods=['GET'])
def hospital():
    """Hospital page"""
    return (render_template('hosp.html'))


# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        print("user_name: ", user_name)
        print("password: ", password)

        if user_name is None or password is None:
            abort(400, description="Missing user_name or password")

        user = storage.get_by(User, userN)
        if user is None:
            abort(404, description="User not found")

        if user.password == password:
            return redirect(url_for('home'))
        else:
            abort(401, description="Invalid password")

    return (render_template('login.html'))

# register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        print("user_name: ", user_name)

        if user_name is None or password is None or user_type is None:
            abort(400, description="Missing user_name or password or user_type")

        user = storage.get_by(User, userN)
        if user is not None:
            abort(409, description="User already exists")

        user = User(user_name=user_name, password=password, user_type=user_type)
        user.save()
        return redirect(url_for('login'))

    return (render_template('register.html'))

@app.route('/person/', methods=['POST', 'GET'])
def create_person():
    """Create a new user"""
    # first_name = request.json.get('first_name')
    # last_name = request.json.get('last_name')
    # gender = request.json.get('gender')
    # phone_number = request.json.get('phone_number')




    if request.method == 'POST':
        print("========Posting===========")
        print("request.form: ", request.form.get('email'))

        email = request.form['email']
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone_number')
        gender = request.json.get('gender')
        
        for field in [email, first_name, last_name, phone, gender]:
            if field is None:
                abort(400, description="Missing field")
            for key in personN_err:
                if request.form.get.get(key) is None:
                    abort(400, description=personN_err[key])

        person_obj = storage.get_by(Person, 'email')
        
        if person_obj.email == email:
            print("========Person exists===========")
            return jsonify(person_obj.to_dict()), 200

        # create new person
        person = Person(email=email, first_name=first_name,
                        last_name=last_name, phone_number=phone)
        person.save()
        print("========Person creted===========")  
    return jsonify(person.to_dict()), 201

# get all people
@app.route('/people', methods=['GET'])
def get_people():
    """Get all users"""
    people = storage.all(Person)

    if people is None:
        abort(404)
    people = [person.to_dict() for person in people.values()]
    return jsonify(people), 200


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())



# get all users
@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = storage.all(User)
    users = [{userN: user.to_dict().get(userN), userT: user.to_dict().get(userT)}\
             for user in users.values()]
    return jsonify(users)


@app.errorhandler(404)
def not_found(error):
    """Return 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host="localhost", port=5000)