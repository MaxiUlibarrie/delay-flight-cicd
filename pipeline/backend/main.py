from fastapi import FastAPI
from pipeline.backend.models import DelayFlightRequest, DelayFlightResponse, DelayFlightModel

from common.log_handler import Logger

logger = Logger()

logger.log.info("Loading model.")
delay_flight_model = DelayFlightModel()

logger.log.info("Getting service up.")
app = FastAPI()

@app.get('/predict-delay-flight', response_model = DelayFlightResponse)
async def predict_delay_flight(df_request: DelayFlightRequest):
    prediction = delay_flight_model.predict(df_request)
    response = { 'prediction' : prediction }

    logger.log.info(f"Prediction for request: {df_request.dict()}")
    logger.log.info(f"Response: {response}")

    return response
