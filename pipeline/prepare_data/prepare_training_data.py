import pandas as pd
import numpy as np
from datetime import datetime

from common.config_handler import Config
from common.log_handler import Logger
from common.data_transformer import normalize_str

logger = Logger()
config = Config()

FEATURE_CATEGORIC_BASIC = list(config.get.base.features.categoric)
TARGET_NAME = config.get.base.features.target

def normalize_columns(data):
    for feature in FEATURE_CATEGORIC_BASIC:
        data[feature] = data[feature].apply(normalize_str)
        data[feature] = data[feature].astype('category')

    return data

def dif_min(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    dif_min = ((fecha_o - fecha_i).total_seconds())/60
    return dif_min

def add_target(data):
    data['dif_min'] = data.apply(dif_min, axis = 1)
    data[TARGET_NAME] = np.where(data['dif_min'] > 15, 1, 0)
    return data

def select_features(data):
    return data[FEATURE_CATEGORIC_BASIC + [TARGET_NAME]]

if __name__ == '__main__':
    logger.log.info("Retrieving data.")
    data = pd.read_csv('./data/dataset_SCL.csv')

    transformations = [
        normalize_columns,
        add_target,
        select_features
    ]

    train_data = data.copy()
    for transform in transformations:
        logger.log.info(f'Applying transformation: {transform.__name__}')
        train_data = transform(train_data)

    logger.log.info("Saving training data.")
    train_data.to_csv("./data/train.csv", index=False)
    