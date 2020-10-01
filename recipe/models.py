from recipe import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean,default=False)
    recipes = db.relationship('Recipe',backref='author')

    def __repr__(self):
        return f"{self.name}"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    upvotes = db.Column(db.Integer,default=False)
    downvotes = db.Column(db.Integer,default=0)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    recipe_steps = db.relationship('RecipeSteps',backref='recipe')
    recipe_ingredients = db.relationship('RecipeIngredients',backref='recipe')

    def __repr__(self):
        return f"{self.name}"

class RecipeSteps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_no = db.Column(db.Integer, nullable=False)
    info = db.Column(db.Text,nullable=False)
    recipe_id = db.Column(db.Integer,db.ForeignKey('recipe.id'))

class RecipeIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String(20))
    name = db.Column(db.Text,nullable=False)
    recipe_id = db.Column(db.Integer,db.ForeignKey('recipe.id'))