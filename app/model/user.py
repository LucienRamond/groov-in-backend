from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    bands = db.relationship('BandMembers', uselist=True, backref='users')

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, bands={self.bands})"