import datetime

from server import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    avatar_img = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    bands = db.relationship('BandMembers', uselist=True, backref='users')
    instruments = db.relationship('UserInstruments', uselist=True, backref='users')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), server_onupdate=datetime.datetime.now(), nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, bands={self.bands}, instruments={self.instruments})"