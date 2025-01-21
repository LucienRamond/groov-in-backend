from app.model.band_members import BandMembers
from app.model.user import User
from app import db
from flask import g, make_response
from flask_restful import fields, marshal_with
from app.model.band import Band
from app.utils.JwtToken import validate_token

userModel = {
    "id": fields.Integer, 
    "name": fields.String
    }
bandModel = {
    "id": fields.Integer, 
    "name": fields.String, 
    "created_by": fields.Nested(userModel),
    "members": fields.List(fields.Nested(userModel))
    }

class BandService():
    @validate_token
    def create_band_service(band_data):
        band = Band(name=band_data["name"], created_by=g.user["id"])
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
        users = User.query.all()

        if not band_query:
            return make_response({"message": "Band not found"}, 404)
        
        band = {
            "id":band_query.id, 
            "name":band_query.name, 
            "created_by": {
                "id":band_query.user.id,
                "name":band_query.user.name
                },
            # A FAIRE !
            "members": [[{"name" : user.name} for user in users if user.id == id] for id in band_query.members_ids]
            }

        return band
    
    @validate_token
    @marshal_with(bandModel)
    def get_my_bands_service():
        bands_query = Band.query.filter_by(created_by=g.user['id']).join(User)
        users_query = User.query.all()

        bands = [{
            "id":band.id, 
            "name":band.name, 
            "created_by":{
                "id":band.user.id,
                "name":band.user.name
                },
            'members': [{'id': member.id, 'name': member.name} for member in users_query]
            } for band in bands_query]
        
        return bands
    
    @marshal_with(bandModel)
    def get_bands_service():
        bands_query = Band.query.outerjoin(BandMembers, BandMembers.band_id == Band.id).join(User, User.id == Band.created_by)
        users_query = User.query.all()

        bands = [{
            "id":band.id, 
            "name":band.name, 
            "created_by": {
                "id":band.user.id,
                "name":band.user.name
                },
            "members": [{'id': member.id, 'name': member.name} for member in users_query]
            } for band in bands_query]
        
        return bands
    
    def edit_band_service(band_data):
        band = Band.query.filter_by(id=band_data['id']).first()

        band.name = band_data["name"]
        band.members_ids = band_data["members_ids"]
        
        db.session.commit()
        
        return make_response({"message":"Band successfully updated"}, 200)