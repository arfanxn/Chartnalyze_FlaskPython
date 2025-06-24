from app.services import CandlestickService
from app.helpers.response_helpers import create_response_tuple
from app.middlewares import authenticated, api_key_verified, email_verified
from app.resources import CandlestickPredictionResource
from flask import Blueprint, request
from http import HTTPStatus

candlestick_service = CandlestickService()

candlestick_bp = Blueprint('candlestick', __name__)

@candlestick_bp.route('/candlesticks/predict', methods=['POST'])
@api_key_verified
@authenticated
@email_verified
def predict():
    image_file = request.files.get('image')
    predictions, = candlestick_service.predict(image_file=image_file)

    return create_response_tuple(
        status=HTTPStatus.OK,
        message=f"Candlestick predicted successfully",
        data={
            'candlestick_predictions': CandlestickPredictionResource.collection(predictions)
        }
    )
