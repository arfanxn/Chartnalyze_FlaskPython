from app.services import Service
from app.actions import PredictCandlestickAction
from werkzeug.exceptions import NotFound

class CandlestickService(Service):

    def __init__(self):
        super().__init__()

    
    def predict(self, image_file: str) -> tuple[list]:
        predict_candlestick = PredictCandlestickAction()
        predictions, = predict_candlestick(image_file=image_file)

        return predictions,