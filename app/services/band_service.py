from app.model.band_members import BandMembers
from app.model.user import User
from app import db
from flask import make_response
from app.model.band import Band
from sqlalchemy.orm import contains_eager

class BandService():
    def get_bands_with_members_query():
        return (
            Band.query          
            .outerjoin(Band.members)
            .outerjoin(BandMembers.users).options(contains_eager(Band.members).contains_eager(BandMembers.users))
        )

    def create_band_service(band_data, user_id):
        band = Band(name=band_data["name"], description=band_data["description"], created_by=user_id)

        db.session.add(band)
        db.session.commit()

        band_member = BandMembers(user_id = user_id, band_id = band.id)
        
        db.session.add(band_member)
        db.session.commit()

        return make_response({"message": "Band successfully created"}, 200)

    def delete_band(user_id, band_id):
        bands = (
            BandService.get_bands_with_members_query()
            .filter(Band.id == band_id)
            .all()
        )
        band = bands[0]

        if band.created_by != user_id:
            return make_response({"message": "Can be deleted only by band creator"}, 404)

        db.session.delete(band)
        db.session.commit()
        
        return make_response({"message": "Band successfully deleted"}, 200)
    
    def get_band_by_id(band_id):
        bands = (
            BandService.get_bands_with_members_query()
            .filter(Band.id == band_id)
            .all()
            )
        
        band = bands[0]

        return {
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
                    } for band in member.users.bands]
                } for member in band.members]
            }
    
    def get_all_bands():
        bands = (
            BandService.get_bands_with_members_query()
            .offset(0)
            .limit(20)
            )

        return [{
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
                    } for band in member.users.bands]
                } for member in band.members]
            } for band in bands]
    
    def update_band(user_id, band_data):
        band = Band.query.filter_by(id=band_data['id']).first()

        if user_id != band.created_by:
            return make_response({"message": "Can be updated only by account owner"}, 403)

        band.name = band_data["name"]
        band.description = band_data["description"]
        
        db.session.commit()
        
        return make_response({"message":"Band successfully updated"}, 200)
    
