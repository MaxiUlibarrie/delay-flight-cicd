from pydantic import create_model, BaseModel
from typing import Literal
import joblib
import pandas as pd
import os

from common.config_handler import Config
from common.log_handler import Logger

logger = Logger()
config = Config()

PREFIX_FEATURE_VALUE = config.get.base.separator_feature_value
REQUEST_FEATURES = vars(config.get.backend.request_features) 

# request features
request_features_param = { k : (eval(v), ...) for k,v in REQUEST_FEATURES.items() } 
DelayFlightRequest = create_model('DelayFlightRequest', **request_features_param)

class DelayFlightResponse(BaseModel):
    prediction: float

class DelayFlightModel():

    def __init__(self):
        logger.log.info("Retrieving and unpackage model.")
        self.model = joblib.load(os.environ.get('MODEL_PATH'))
        self.feature_names = self.model.feature_names_final

    def predict(self, df_request: DelayFlightRequest):
        x = self.__transform_input(df_request)
        prediction = self.model.predict(x)[0]
        return prediction
        
    def __transform_input(self, df_request: DelayFlightRequest):
        req = df_request.dict()
        mask_features = [ PREFIX_FEATURE_VALUE.join([k,v]) for k,v in req.items() ]
        x = { k : ([1] if k in mask_features else [0]) for k in self.feature_names }
        x = pd.DataFrame.from_dict(x)
        
        return x
