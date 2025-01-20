from app.model.user import User
from app.services.user_service import UserService
from app import db
from flask import g, make_response
from flask_restful import fields, marshal_with
from app.model.band import Band
from app.utils.JwtToken import validate_token

leaderModel = {
    "id": fields.Integer, 
    "name": fields.String
    }
bandModel = {
    "id": fields.Integer, 
    "name": fields.String, 
    "leader": fields.Nested(leaderModel)
    }

class BandService():
    @validate_token
    def create_band_service(band_data):
        band = Band(name=band_data["name"], user_id=g.user["id"])
        db.session.add(band)
        db.session.commit()
        return make_response({"message": "Band successfully created"}, 200)

    @validate_token
    def delete_band_service(band_id):
        band = Band.query.filter_by(id=band_id).first()
        user = User.query.filter_by(id=g.user["id"]).first()

        if band not in user.bands:
            return make_response({"message": "Can be deleted only by owner"}, 404)
        
        db.session.delete(band)
        db.session.commit()
        
        return make_response({"message": "Band successfully deleted"}, 200)
    
    def get_band_service(band_id):
        band_query = Band.query.filter_by(id=band_id).join(User).first()

        if not band_query:
            return make_response({"message": "Band not found"}, 404)
        
        band = {
            "id":band_query.id, 
            "name":band_query.name, 
            "leader": {
                "id":band_query.user.id,
                "name":band_query.user.name
                }
            }

        return band
    
    @validate_token
    @marshal_with(bandModel)
    def get_my_bands_service():
        bands_query = Band.query.filter_by(user_id=g.user['id']).join(User) 
        bands = [{
            "id":band.id, 
            "name":band.name, 
            "leader": {
                "id":band.user.id,
                "name":band.user.name
                }
            } for band in bands_query]
        
        return bands
    
    @marshal_with(bandModel)
    def get_bands_service():
        bands_query = Band.query.join(User)
        bands = [{
            "id":band.id, 
            "name":band.name, 
            "leader": {
                "id":band.user.id,
                "name":band.user.name
                }
            } for band in bands_query]
        
        return bands