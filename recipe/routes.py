from flask import render_template, url_for, flash, redirect
from random import randint
from recipe import app, db
from recipe.models import Name

@app.route('/')
def home():
    n = Name(str(randint(1,999)))
    db.session.add(n)
    db.session.commit()
    return "Hello"
