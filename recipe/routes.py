from flask import jsonify, Flask, request, make_response, g
from sqlalchemy import func
from recipe import app, db, auth
from recipe.models import *
from recipe.utils import *


@app.route('/')
def home():
    return jsonify({'message': "Welcome"})

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
        return jsonify({'error': 'User not found'})
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
    try:
        username = request.json.get('username')
        name = request.json.get('name')
        password = request.json.get('password')
        if username is None or password is None or name is None:
            return jsonify({'error': "Please provide valid data"})
        if User.query.filter_by(username=username).first() is not None:
            return jsonify({'error': "Username not available"})
        user = User(username=username, name=name)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': "User Created"})
    except:
        return jsonify({'error': "Please provide valid data"})


# Delete an user


@ app.route('/users/<username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    # Not admin and not the user itself
    if not (g.user.admin or g.user.username == username):
        return jsonify({'error': f'Only admin or {username} can delete'})
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': "User Deleted"})


# Get Random Recipes

@app.route('/recipes', methods=['GET'])
@app.route('/recipes/random', methods=['GET'])
def get_recipes_random():
    count = request.args.get('count', 10, type=int)
    recipes = Recipe.query.order_by(func.random()).limit(10)
    op = recipes2JSON(recipes)
    return jsonify({'recipes': op})

# Get recipe by id


@app.route('/recipes/<id>', methods=['GET'])
def get_recipe(id):
    recipes = [Recipe.query.get(id)]
    if not recipes[0]:
        return jsonify({'error': "Recipe not found"})
    op = recipes2JSON(recipes)
    return jsonify({'recipes': op})

# Get new recipes


@app.route('/recipes/new', methods=['GET'])
def get_recipes_by_new():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 10, type=int)
    desc = request.args.get('desc', True, type=bool)
    if desc:
        sortby = Recipe.created_date.desc()
    else:
        sortby = Recipe.created_date.asc()
    recipes = Recipe.query.order_by(sortby).paginate(page=page, per_page=count)
    op = recipes2JSON(recipes)
    return jsonify({'recipes': op})


# Get top recipes


@app.route('/recipes/top', methods=['GET'])
def get_recipes_by_top():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 10, type=int)
    desc = request.args.get('desc', True, type=bool)
    if desc:
        sortby = Recipe.likes.desc()
    else:
        sortby = Recipe.likes.asc()
    recipes = Recipe.query.order_by(sortby).paginate(page=page, per_page=count)
    op = recipes2JSON(recipes)
    return jsonify({'recipes': op})


# Add new recipe

@app.route('/recipes', methods=['POST'])
@auth.login_required
def add_recipes():
    try:
        name = request.json.get('name')
        username = request.json.get('username')
        ingredients = request.json.get('ingredients')
        steps = request.json.get('steps')
        images = request.json.get('images')
        author_id = User.query.filter_by(username=username).first().id
        new_recipe(name, author_id, ingredients, steps, images)
        db.session.commit()
        return jsonify({'message': "Added"})
    except:
        db.session.rollback()
        return jsonify({'error': "Cannot add recipe. Please check if data is entered correctly"})


# Delete an recipe


@ app.route('/recipes/<id>', methods=['DELETE'])
@auth.login_required
def delete_recipe(id):
    recipe_ref = Recipe.query.get(id)
    if not recipe_ref:
        return jsonify({'error': 'Recipe not found'})

    # Not admin and not the user itself
    if not (g.user.admin or g.user.username == recipe_ref.author.username):
        return jsonify({'error': f'Only admin or {username} can delete'})
    db.session.delete(recipe_ref)
    db.session.commit()
    return jsonify({'message': "Recipe Deleted"})

# Get recipes of a user


@app.route('/recipes/user/<username>', methods=['GET'])
def user_recipes(username):
    try:
        user = User.query.filter_by(username=username).first()
        op = recipes2JSON(user.recipes)
        return jsonify({'recipes': op})
    except:
        return jsonify({'error': f"Cannot fetch recipes of user {username}"})
