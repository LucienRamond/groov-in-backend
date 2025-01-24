import os
from app.model.band import Band
from app import db
from app.model.band_members import BandMembers
from app.model.user import User
from flask import app, make_response, g
from flask_restful import fields, marshal_with
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from app.utils.JwtToken import generate_token, validate_token
from sqlalchemy.orm import contains_eager

SECRET = os.environ.get('SECRET_KEY')

bandModel = {"id": fields.Integer, "name": fields.String}
userModel = {"id": fields.Integer, "name": fields.String, "description": fields.String, "email": fields.String, "bands": fields.List(fields.Nested(bandModel))}

class UserService():
    @marshal_with(userModel)
    def get_user_service(id):
        user = User.query.filter_by(id=id).join(BandMembers).first()

        user = {
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "description":user.description,
            "bands":[{
                'id':band.bands.id,
                'name':band.bands.name} for band in user.bands]
        }

        return user
    
    @marshal_with(userModel)
    def get_current_user_service(user_id):
        user = User.query.filter_by(id=user_id).join(BandMembers).first()
        bands = BandMembers.query.join(Band, Band.id == BandMembers.band_id).options(contains_eager(BandMembers.bands)).all()

        response = {
            "id":user.id, 
            "name":user.name, 
            "email":user.email,
            "description":user.description,
            "members": [{
                'id': member.users.id, 
                'name': member.users.name, 
                'bands': [{
                    'id': band.bands.id, 
                    "name": band.bands.name
                    } for band in bands if band.user_id == member.users.id]
                } for member in user.bands]
            }
        return response
    
    def edit_current_user_service(user_data, user_id):

        if user_id != user_data["id"]:
            return make_response({"message": "Can be updated only by account owner"}, 404)
          
        user = User.query.filter_by(id=user_id).first()

        user.name = user_data["name"]
        user.email = user_data["email"]
        user.description = user_data["description"]
        db.session.commit()

        response = make_response({"id": user.id, "name": user.name}, 200)

        return response
    
    @marshal_with(userModel)
    def get_users_service():
        users = User.query.all()
        response = [{
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "description":user.description,
            "bands":[{
                "id":band.bands.id,
                "name":band.bands.name,
                } for band in user.bands
            ]
        } for user in users]
        return response
    
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
