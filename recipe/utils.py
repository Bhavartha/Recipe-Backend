from recipe import auth
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
            'steps': steps2JSON(r.recipe_steps)
        })
        print()
    return op