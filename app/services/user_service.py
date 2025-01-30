import os
from app.model.band import Band
from app import db
from app.model.band_members import BandMembers
from app.model.instrument import Instrument
from app.model.user import User
from flask import make_response
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from app.model.user_instruments import UserInstruments
from app.utils.JwtToken import generate_token, validate_token
from sqlalchemy.orm import contains_eager

SECRET = os.environ.get('SECRET_KEY')

class UserService():
    def get_users_with_bands_and_instruments_query():
        return (
            User.query
            .outerjoin(User.bands)
            .outerjoin(BandMembers.bands).options(contains_eager(User.bands).contains_eager(BandMembers.bands))            
            .outerjoin(User.instruments)
            .outerjoin(UserInstruments.instruments).options(contains_eager(User.instruments).contains_eager(UserInstruments.instruments))
        )

    def get_user_by_id(user_id):
        users = (
            UserService.get_users_with_bands_and_instruments_query()
            .filter(User.id == user_id)
            .all()
        )

        if len(users) == 0:
            return make_response({"message": f"User {user_id} not found "}, 404)

        user = users[0]

        return {
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "description":user.description,
            "instruments": [{
                'id':instrument.instruments.id, 
                'name':instrument.instruments.name
            } for instrument in user.instruments],
            "bands":[{
                'id':band.bands.id, 
                'name':band.bands.name
            } for band in user.bands]
        }
    
    def update_user(user_id, user_data):

        if user_id != user_data["id"]:
            return make_response({"message": "Can be updated only by account owner"}, 403)
          
        user = User.query.filter_by(id=user_id).first()

        # TODO remove only instruments to remove
        # TODO remove all instruments in one query(delete in)
        for instrument in user.instruments:
            db.session.delete(instrument)

        # TODO remove only instruments to remove
        # TODO remove only instruments in one query
        for instrument_id in user_data["instruments"]:
            user_instrument = UserInstruments(user_id=user_id, instrument_id=instrument_id)
            db.session.add(user_instrument) 

        user.name = user_data["name"]
        user.email = user_data["email"]
        user.description = user_data["description"]

        db.session.commit()

        response = make_response({"id": user.id, "name": user.name}, 200)

        return response
    
    def get_all_users():
        users = (
            UserService.get_users_with_bands_and_instruments_query()
            .offset(0)
            .limit(20)
        )

        return [{
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "description":user.description,
            "instruments":[{
                "id":band.instruments.id,
                "name":band.instruments.name,
                } for band in user.instruments if user.instruments
            ],
            "bands":[{
                "id":band.bands.id,
                "name":band.bands.name,
                } for band in user.bands if user.bands
            ]
        } for user in users]
    
    def signup_service(user_data):
        try:
            email_check = User.query.filter_by(email=user_data["email"]).first()
            if email_check:
                return {"status": 404, "message": "Email already exists"}
            else:
                user = User(name=user_data["name"], email=user_data["email"], password_hash=generate_password_hash(user_data["password"]))
                db.session.add(user)
                db.session.commit()
                return make_response({'message': 'Successfully signed up'}, 201)
        except Exception as e:
            return make_response({'message': str(e)}, 404)
        
    def login_service(user_credentials):
        try:

            user = User.query.filter_by(email=user_credentials["email"]).first()

            if not user:
                return make_response({'message': 'User not found'}, 404)
            else:
                payload = {"_id": str(user.id), 'exp': datetime.datetime.now() + datetime.timedelta(minutes=60)}
                if check_password_hash(user.password_hash, user_credentials["password"]):
                    token = generate_token(payload, SECRET)
                    response = make_response({"id": user.id, "name": user.name}, 200)
                    response.set_cookie("token",token)
                    return response
                else:
                    return make_response({'message':'Invalid password'}, 403)

        except Exception as e:
            return make_response({'message': str(e)}, 404)
        
    def logout_service():
        response = make_response({'message': 'Successfully logged out'}, 200)
        response.delete_cookie("token")
        return response
        
    def reset_password_service(password_data, user_id):
        if user_id != password_data["id"] :
            return make_response({'message': "Only updating by logged user"}, 403)

        user = User.query.filter_by(id=user_id).first()

        if not user:
            return make_response({'message': "User not found"}, 403)
        
        if check_password_hash(user.password_hash, password_data["old_password"]):
            user.password_hash = generate_password_hash(password_data["new_password"])
            db.session.commit()
        else:
            return make_response({'message': 'Invalid old password'}, 403)

        return make_response({'message': 'Successfully updated password'}, 200)
    
    def get_user_bands(user_id):
        users = (
            UserService.get_users_with_bands_and_instruments_query()
            .filter(User.id == user_id)
            .all()
        )

        if len(users) == 0:
            return make_response({"message": f"User {user_id} not found "}, 404)

        user = users[0]

        return [{
            "id":band.bands.id, 
            "name":band.bands.name,
            "description": band.bands.description,
            "created_by": [{
                "id":user.users.id,
                "name":user.users.name
                } for user in band.bands.members if user.users.id == user.bands.created_by],
            "members": [{
                'id': member.users.id, 
                'name': member.users.name, 
                'bands': [{
                    'id': band.bands.id, 
                    "name": band.bands.name
                    } for band in member.users.bands]
                } for member in band.bands.members]
            } for band in user.bands]