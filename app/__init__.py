from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = "qwertyuioplkmjnha5526735gbsgsg"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)

from app.model.band import Band
from app.model.user import User
from app.model.instrument import Instrument
from app.model.band_members import BandMembers
from app.model.user_instruments import UserInstruments

with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True)

from app.api.user import user_route
app.register_blueprint(user_route)
from app.api.band import band_route
app.register_blueprint(band_route)
from app.api.instrument import instrument_route
app.register_blueprint(instrument_route)

if '__name__' == '__main__':
    app.run()