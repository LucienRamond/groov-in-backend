from flask import Blueprint, g, request
from app.services.band_service import BandService
from app.services.user_service import UserService
from app.utils.JwtToken import validate_token

band_route = Blueprint('band_route', __name__)


@band_route.route('/bands/create', methods=['POST'])
@validate_token
def create():
    data = request.get_json()
    return BandService.create_band_service(data, g.user["id"])

@band_route.route('/bands/delete/<int:band_id>', methods=['DELETE'])
@validate_token
def delete(band_id):
    return BandService.delete_band(g.user['id'], band_id)

@band_route.route('/bands/<int:band_id>', methods=['GET'])
def get_band(band_id):
    return BandService.get_band_by_id(band_id)

@band_route.route('/bands/my-bands', methods=['GET'])
@validate_token
def get_my_band():
    return UserService.get_user_bands(g.user['id'])

@band_route.route('/bands', methods=['GET'])
def get_bands():
    return BandService.get_all_bands()

@band_route.route('/bands/edit', methods=['PUT'])
@validate_token
def edit_band():
    data = request.get_json()
    return BandService.edit_band_service(data, g.user['id'])
