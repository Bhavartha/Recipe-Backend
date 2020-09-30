from url_shortener import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_link = db.Column(db.Text, nullable=False)
    full_link = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"{self.full_link}:{self.short_link}"
