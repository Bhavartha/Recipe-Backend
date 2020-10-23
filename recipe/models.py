import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from recipe import db,app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    recipes = db.relationship('Recipe', backref='author')

    # Return string representation on User Object 
    def __repr__(self):
        return f"{self.name}"

    # Hashing the password
    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)
    
    # Verify the password given is correct
    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    # Genreate auth token so that client can use auth token to authenticate itself instead of sending password every request
    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # Function to verify if the recieved token is valid
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_steps = db.relationship('RecipeSteps', backref='recipe')
    recipe_ingredients = db.relationship('RecipeIngredients', backref='recipe')
    recipe_images = db.relationship('RecipeImages', backref='recipe')

    def __repr__(self):
        return f"{self.name}"


class RecipeSteps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_no = db.Column(db.Integer, nullable=False)
    info = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


class RecipeIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String(10))
    name = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

class RecipeImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_data = db.Column(db.Text,nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
