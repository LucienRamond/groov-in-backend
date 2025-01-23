from app.model.band_members import BandMembers
from app.model.user import User
from app import db
from flask import g, make_response
from flask_restful import fields, marshal_with
from app.model.band import Band
from sqlalchemy.orm import contains_eager

userModel = {
    "id": fields.Integer, 
    "name": fields.String,
    }
bandModel = {
    "id": fields.Integer, 
    "name": fields.String,
    "description": fields.String,
    "created_by": fields.Nested(userModel),
    "members": fields.List(fields.Nested(userModel))
    }

class BandService():

    def create_band_service(band_data, user_id):
        band = Band(name=band_data["name"], description=band_data["description"], created_by=user_id)
        db.session.add(band)
        db.session.commit()
        band_members = BandMembers(band_id=band.id,user_id=user_id)
        db.session.add(band_members)
        db.session.commit()
        return make_response({"message": "Band successfully created"}, 200)

    def delete_band_service(band_id):
        band = Band.query.filter_by(id=band_id).first()
        user = User.query.filter_by(id=g.user["id"]).first()

        if band not in user.bands:
            return make_response({"message": "Can be deleted only by owner"}, 404)
        
        db.session.delete(band)
        db.session.commit()
        
        return make_response({"message": "Band successfully deleted"}, 200)
    
    marshal_with(bandModel)
    def get_band_service(band_id):
        band = Band.query.filter_by(id=band_id).join(BandMembers).first()
        bands = BandMembers.query.join(Band, Band.id == BandMembers.band_id).options(contains_eager(BandMembers.bands)).all()

        response = {
            "id":band.id, 
            "name":band.name,
            "description": band.description,
            "created_by": [{
                "id":user.users.id,
                "name":user.users.name
                } for user in band.members if user.users.id == user.bands.created_by],
            "members": [{
                'id': member.users.id, 
                'name': member.users.name, 
                'bands': [{
                    'id': band.bands.id, 
                    "name": band.bands.name
                    } for band in bands if band.user_id == member.users.id]
                } for member in band.members]
            }
        
        return response
    
    @marshal_with(bandModel)
    def get_my_bands_service(user_id):
        bands = Band.query.join(BandMembers).filter_by(user_id=user_id)

        bands = [{
            "id":band.id, 
            "name":band.name,
            "description": band.description,
            "created_by": [{
                "id":user.users.id,
                "name":user.users.name
                } for user in band.members if user.users.id == band.created_by],
            "members": [{'id': member.users.id, 'name': member.users.name} for member in band.members]
            } for band in bands]
        
        return bands
    
    @marshal_with(bandModel)
    def get_bands_service():
        bands_query = Band.query.all()

        bands = [{
            "id":band.id, 
            "name":band.name,
            "description": band.description, 
            "created_by": [{
                "id":user.users.id,
                "name":user.users.name
                } for user in band.members if user.users.id == band.created_by],
            "members": [{'id': member.users.id, 'name': member.users.name} for member in band.members]
            } for band in bands_query]
        
        return bands
    
    def edit_band_service(band_data):
        band = Band.query.filter_by(id=band_data['id']).first()

        band.name = band_data["name"]
        band.members_ids = band_data["members_ids"]
        
        db.session.commit()
        
        return make_response({"message":"Band successfully updated"}, 200)