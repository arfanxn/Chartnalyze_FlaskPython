from app.actions.action import Action
from app import extensions
from PIL import Image
from werkzeug.exceptions import UnprocessableEntity
import types
import io

class PredictCandlestickAction(Action):
    def __init__(self):
        super().__init__()

    def __call__(
            self, 
            image_file,
        ) -> tuple[list]:
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        model = extensions.candlestick_ml_model

        results = model(image, verbose=False)

        predictions = []
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            coords = box.xyxy[0].tolist()
            bounding_box = {
                    'x1': round(coords[0]),
                    'y1': round(coords[1]),
                    'x2': round(coords[2]),
                    'y2': round(coords[3]),
            }

            prediction = types.SimpleNamespace(
                class_id = class_id,
                class_name = model.names[class_id],
                confidence = confidence,
                bounding_box = bounding_box
            )

            predictions.append(prediction)

        if len(predictions) == 0:
            raise UnprocessableEntity({'image' : ['Image does not contain any candlestick or failed to predict']})
            
        return predictions, 