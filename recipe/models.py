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
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.name}"
