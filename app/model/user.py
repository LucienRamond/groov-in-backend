from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    bands = db.relationship('Band', backref='user', lazy=True)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, band={self.bands})"