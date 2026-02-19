from flask import Blueprint

from services.instrument_service import InstrumentService

instrument_route = Blueprint('instrument_route', __name__)

@instrument_route.route('/instruments', methods=['GET'])
def get_users():
    return InstrumentService.get_instruments_service()