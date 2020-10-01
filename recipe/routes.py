from flask import jsonify
from recipe import app, db
from recipe.models import *

@app.route('/')
def home():
    return jsonify({1:"hello"})
