import pandas as pd
import numpy as np
from datetime import datetime

from pipeline.train.models import DataTransformer, DataPreparer

from common.config_handler import Config
from common.log_handler import Logger

logger = Logger()
config = Config()

FEATURE_CATEGORIC_BASIC = list(config.get.base.features.categoric)
TARGET_NAME = config.get.base.features.target

def prepare_train_data():
    logger.log.info("Retrieving data.")
    data = pd.read_csv('./data/dataset_SCL.csv')

    data_preparer = DataPreparer([
        NormalizeColumns(),
        AddTarget(),
        SelectFeatures()
    ])

    train_data = data_preparer.prepare_data(data)

    logger.log.info("Saving training data.")
    train_data.to_csv("./data/train.csv", index=False)


class NormalizeColumns(DataTransformer):

    def transform(self, data):
        for feature in FEATURE_CATEGORIC_BASIC:
            data[feature] = data[feature].apply(NormalizeColumns.normalize_str)
            data[feature] = data[feature].astype('category')

        return data
    
    def normalize_str(x):
        x = str(x)
        x = x.upper()
        x = x.replace(',','')
        x = ' '.join(x.split())
        x = x.replace(' ','_')
        return x
    
class AddTarget(DataTransformer):

    def transform(self, data):
        data['dif_min'] = data.apply(AddTarget.dif_min, axis = 1)
        data[TARGET_NAME] = np.where(data['dif_min'] > 15, 1, 0)
        return data
    
    def dif_min(data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        dif_min = ((fecha_o - fecha_i).total_seconds())/60
        return dif_min

class SelectFeatures(DataTransformer):

    def transform(self, data):
        return data[FEATURE_CATEGORIC_BASIC + [TARGET_NAME]]
    