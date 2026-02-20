import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, g, request
from services.user_service import UserService
from utils.JwtToken import validate_token

user_route = Blueprint('user_route', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_route.route('/user/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return UserService.signup_service(data)

@user_route.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    return UserService.login_service(data)

@user_route.route('/user/logout', methods=['GET'])
def logout():
    return UserService.logout_service()

@user_route.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserService.get_user_by_id(user_id)

@user_route.route('/user/@me', methods=['GET'])
@validate_token
def get_current_user():
    return UserService.get_user_by_id(g.user["id"])

@user_route.route('/user/reset-password', methods=['PATCH'])
@validate_token
def reset_user_password():
    data = request.get_json()
    return UserService.reset_password_service(data, g.user["id"])

@user_route.route('/user/edit', methods=['PATCH'])
@validate_token
def edit_current_user():
    data = request.get_json()
    return UserService.update_user(g.user["id"], data)

@user_route.route('/user/avatar/<string:avatar_name>', methods=['GET'])
def get_avatar(avatar_name):
    return UserService.get_avatar_by_name(avatar_name)

@user_route.route('/user/edit/avatar', methods=['POST'])
@validate_token
def edit_user_avatar():
    file = request.files["file"]
    if allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        name, extension = os.path.splitext(file_name)
        return UserService.update_user_avatar(g.user["id"], file, (f'{str(uuid.uuid4())}{extension}'))

@user_route.route('/users', methods=['GET'])
def get_users():
    return UserService.get_all_users()