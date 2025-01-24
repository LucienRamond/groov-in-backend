from app.model.instrument import Instrument
from flask_restful import fields, marshal_with

instrumentModel = { "id":fields.Integer, "name": fields.String}

class InstrumentService():
    
    @marshal_with(instrumentModel)
    def get_instruments_service():
        instruments = Instrument.query.all()
        response = [{"id":instrument.id, "name":instrument.name} for instrument in instruments]
        return response