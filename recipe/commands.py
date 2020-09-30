from flask.cli import with_appcontext
import click

from recipe import app,db
from recipe.models import *

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()