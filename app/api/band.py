from flask import Blueprint, request
from app.services.band_service import BandService
from app.utils.JwtToken import validate_token
band_route = Blueprint('band_route', __name__)

@band_route.route('/bands/create', methods=['POST'])
def create():
    data = request.get_json()
    return BandService.create_band_service(data)

@band_route.route('/bands/delete/<int:id>', methods=['DELETE'])
def delete(id):
    return BandService.delete_band_service(id)

@band_route.route('/bands/<int:band_id>', methods=['GET'])
def get_band(band_id):
    return BandService.get_band_service(band_id)

@band_route.route('/bands/my-bands', methods=['GET'])
def get_my_band():
    return BandService.get_my_bands_service()

@band_route.route('/bands', methods=['GET'])
def get_bands():
    return BandService.get_bands_service()

@band_route.route('/bands/edit', methods=['PUT'])
def edit_band():
    data = request.get_json()
    return BandService.edit_band_service(data)
