from flask import Blueprint, g, request
from flask_cors import cross_origin
from app.services.user_service import UserService
from app.utils.JwtToken import validate_token

user_route = Blueprint('user_route', __name__)

@user_route.route('/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return UserService.signup_service(data)

@user_route.route('/user/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    return UserService.login_service(data)

@user_route.route('/user/logout', methods=['GET'])
@cross_origin(supports_credentials=True)
def logout():
    return UserService.logout_service()

@user_route.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserService.get_user_service(user_id)


@user_route.route('/user/@me', methods=['GET'])
@validate_token
def get_current_user():
    return UserService.get_current_user_service(g.user["id"])

@user_route.route('/user/edit', methods=['PATCH'])
def edit_current_user():
    data = request.get_json()
    return UserService.edit_current_user_service(data)

@user_route.route('/users', methods=['GET'])
def get_users():
    return UserService.get_users_service()