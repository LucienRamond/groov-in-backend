from server import db

class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    users = db.relationship('UserInstruments', uselist=True, backref='instruments')

    def __repr__(self):
        return str(self.id)