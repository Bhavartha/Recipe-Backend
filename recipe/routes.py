from flask import render_template, url_for, flash, redirect

from recipe import app, db


@app.route('/')
def home():
