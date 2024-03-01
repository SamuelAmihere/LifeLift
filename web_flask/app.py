#! /usr/bin/env python3
"""This is flask app"""
import hashlib
import os

from flask import Flask, jsonify, make_response, render_template, request, abort
from models import storage
from models import storage_type
from models.system_user import Person
from models.user import User

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
def home():
    """Home page"""
    return (render_template('index.html'))


@app.route('/person/', methods=['POST', 'GET'])
def person():
    """Create a new user"""
    # first_name = request.json.get('first_name')
    # last_name = request.json.get('last_name')
    # gender = request.json.get('gender')
    # phone_number = request.json.get('phone_number')

    req_json = request.get_json()
    if req_json is None:
        abort(400, description="Not a JSON")
    
    if request.method == 'POST':
        for key in personN_err:
            if req_json.get(key) is None:
                abort(400, description=personN_err[key])

        person_obj = storage.get_by(Person, 'email')
        
        if person_obj.email == req_json.get('email'):
            print("========Person exists===========")
            return jsonify(person_obj.to_dict()), 200

        # create new person
        person = Person(**request.json)
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