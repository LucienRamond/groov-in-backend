from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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