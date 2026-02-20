import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DEPLOY_DATABASE_URI")
app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")

db = SQLAlchemy(app)

from model.band import Band
from model.user import User
from model.instrument import Instrument
from model.band_members import BandMembers
from model.user_instruments import UserInstruments

with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True)

from api.user import user_route
app.register_blueprint(user_route)
from api.band import band_route
app.register_blueprint(band_route)
from api.instrument import instrument_route
app.register_blueprint(instrument_route)

if __name__ == '__main__':
    app.run()