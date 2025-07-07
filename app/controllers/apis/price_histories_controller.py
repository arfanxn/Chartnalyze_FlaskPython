from app.services import PriceHistoriesService
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import api_key_verified
from app.resources import PriceHistoryResource
from flask import Blueprint
from http import HTTPStatus

ph_service = PriceHistoriesService()

ph_bp = Blueprint('price_history', __name__)
price_history_bp = ph_bp

@ph_bp.route('/price_histories/<string:symbol>', methods=['GET'])
@api_key_verified
def all_by_symbol(symbol: str):
    
    price_histories, = ph_service.all_by_symbol(symbol=symbol)
    price_histories_json = PriceHistoryResource.collection(price_histories)
    
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Price histories retrieved successfully',
        data={'price_histories': price_histories_json},
    )

@ph_bp.route('/price_histories/symbols', methods=['GET'])
@api_key_verified
def all_distinct_symbols():
    symbols, = ph_service.all_distinct_symbols()
    
    return create_response_tuple(
        status=HTTPStatus.OK,
        message='Symbols retrieved successfully',
        data={'symbols': symbols},
    )
