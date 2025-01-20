import os

from app.model.band import Band
from app import db
from app.model.user import User
from flask import app, make_response, g
from flask_restful import fields, marshal_with
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from app.utils.JwtToken import generate_token, validate_token

SECRET = os.environ.get('SECRET_KEY')

creatorModel = {"id": fields.Integer, "name": fields.String}
bandModel = {"id": fields.Integer, "name": fields.String, "creator": fields.Nested(creatorModel)}
userModel = {"id": fields.Integer, "name": fields.String, "email": fields.String, "bands": fields.List(fields.Nested(bandModel))}

class UserService():
    @marshal_with(userModel)
    def get_user_service(id):
        user_query = User.query.filter_by(id=id).join(Band).first()
        user = {
            "id":user_query.id,
            "name":user_query.name,
            "email":user_query.email,
            "bands":[{
                "id":band.id,
                "name":band.name,
                "leader": {
                    "id":band.user.id,
                    "name":band.user.name
                }} for band in user_query.bands
            ]
        }

        return user
    
    @validate_token    
    @marshal_with(userModel)
    def get_current_user_service():
        user_query = User.query.filter_by(id=g.user["id"]).join(Band).first()
        user = {
            "id":user_query.id,
            "name":user_query.name,
            "email":user_query.email,
            "bands":[{
                "id":band.id,
                "name":band.name,
                "leader": {
                    "id":band.user.id,
                    "name":band.user.name
                }} for band in user_query.bands
            ]
        }

        return user
    
    @validate_token
    def edit_current_user_service(user_data):
        user = User.query.filter_by(id=g.user["id"]).first()
        if user.id != user_data["id"]:
            return make_response({"message": "Can be updated only by account owner"}, 404)
        
        user.name = user_data["name"]
        user.email=user_data["email"]
        db.session.commit()

        return make_response({"message": "User successfully updated"})
    
    @marshal_with(userModel)
    def get_users_service():
        users_query = User.query.all()
        users = [{
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "bands":[{
                "id":band.id,
                "name":band.name,
                "leader": {
                    "id":band.use.id,
                    "name":band.use.name
                }} for band in user.bands
            ]
        } for user in users_query]
        return users
    
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
                    response = make_response({"message": "Login Successfully"}, 200)
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
