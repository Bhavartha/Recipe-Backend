from recipe import auth, db
from recipe.models import *

from flask import g


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def ingredients2JSON(ingredients):
    op = []
    for i in ingredients:
        op.append({
            'name': i.name,
            'quantity': i.quantity
        })
    return op


def steps2JSON(steps):
    op = []
    for s in steps:
        op.append({
            'step_no': s.step_no,
            'info': s.info
        })
    return op


def images2JSON(images):
    return [i.img_data for i in images]


def recipes2JSON(recipes):
    op = []
    for r in recipes:
        op.append({
            'name': r.name,
            'likes': r.likes,
            'created_date': r.created_date,
            'author': r.author.name,
            'author_username': r.author.username,
            'ingredients': ingredients2JSON(r.recipe_ingredients),
            'steps': steps2JSON(r.recipe_steps),
            'images': images2JSON(r.recipe_images)
        })
    return op


def new_recipe(name, author_id, ingredients, steps, images):
    recipe = Recipe(name=name, author_id=author_id)
    db.session.add(recipe)
    db.session.flush()
    if ingredients is None or steps is None:
        raise Exception()
    for i in ingredients:
        quantity = i.get('quantity')
        name = i.get('name')
        ri = RecipeIngredients(
            name=name, quantity=quantity, recipe_id=recipe.id)
        db.session.add(ri)
    print("ING")
    for s in steps:
        step_no = s.get('step_no')
        info = s.get('info')
        rs = RecipeSteps(step_no=step_no, info=info, recipe_id=recipe.id)
        db.session.add(rs)
    print("STP")
    for i in images:
        ri = RecipeImages(img_data=i, recipe_id=recipe.id)
        db.session.add(ri)
    print("IMG")
