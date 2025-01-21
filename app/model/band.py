from app import db

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members = db.relationship('BandMembers', uselist=True, backref='bands')

    def __repr__(self):
        return str(self.id)