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
            'public_id': user.public_id,
            'name': user.name,
            'password': user.password,
            'admin': user.admin,
        })
    return jsonify({'users': op})


@app.route('/users/<public_id>', methods=['GET'])
def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    op = {
            'public_id': user.public_id,
            'name': user.name,
            'password': user.password,
            'admin': user.admin,
        }
    return jsonify({'user': op})


@ app.route('/users', methods = ['POST'])
def add_user():
    data=request.get_json()
    hashed_password=generate_password_hash(data['password'], method = 'sha256')
    user=User(public_id = str(uuid.uuid4()),
                name = data['name'],
                password = hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': "User Created"})


@ app.route('/users/<public_id>', methods = ['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': "User Deleted"})

