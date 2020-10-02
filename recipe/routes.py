import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, Flask, request

from recipe import app, db
from recipe.models import *


@app.route('/')
def home():
    return "Hello"


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    op = []
    for user in users:
        op.append({
            'username': user.username,
            'name': user.name,
            'password': user.password,
            'admin': user.admin,
        })
    return jsonify({'users': op})


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'})
    op = {
            'username': user.username,
            'name': user.name,
            'password': user.password,
            'admin': user.admin,
        }
    return jsonify({'user': op})


@ app.route('/users', methods = ['POST'])
def add_user():
    data=request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'Username taken'})
    hashed_password=generate_password_hash(data['password'], method = 'sha256')
    user=User(username = data['username'],
                name = data['name'],
                password = hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': "User Created"})


@ app.route('/users/<username>', methods = ['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': "User Deleted"})

