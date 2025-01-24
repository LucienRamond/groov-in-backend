from app import db

class BandMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return str(self.id)