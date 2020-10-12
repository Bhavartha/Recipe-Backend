from flask import jsonify, Flask, request, make_response, g

from recipe import app, db, auth
from recipe.models import *
from recipe.utils import *


@app.route('/')
def home():
    return jsonify({'msg': "Welcome"})

# Get all users


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    op = []
    for user in users:
        op.append({
            'username': user.username,
            'name': user.name,
            'admin': user.admin,
        })
    return jsonify({'users': op})

# Get a specific user


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'})
    op = {
        'username': user.username,
        'name': user.name,
        'admin': user.admin,
    }
    return jsonify({'user': op})

# Get auth token


@app.route('/auth_token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

# Add new user


@ app.route('/users', methods=['POST'])
def add_user():
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')
    if username is None or password is None or name is None:
        jsonify({'error': "Please provide valid data"})
    if User.query.filter_by(username=username).first() is not None:
        jsonify({'error': "Username not available"})
    user = User(username=username, name=name)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': "User Created"})

@auth.login_required
@ app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    print(g.user.isAdmin())
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'})
    # db.session.delete(user)
    # db.session.commit()
    return jsonify({'message': "User Deleted"})

