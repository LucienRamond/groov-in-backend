from app import db

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members_ids = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return str(self.id)