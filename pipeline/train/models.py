from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from common.log_handler import Logger

logger = Logger()

class DataTransformer(ABC):

    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    def __str__(self):
        return self.__class__.__name__

class DataPreparer():

    def __init__(self, data_transformers: List[DataTransformer] = []):
        self.data_transformers = data_transformers

    def add_data_transformer(self, data_transformer: DataTransformer):
        self.data_transformers.append(data_transformer)
        return self

    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        prepared_data = data.copy()
        for dt in self.data_transformers:
            logger.log.info(f'Applying transformation: {dt}')
            prepared_data = dt.transform(prepared_data)

        return prepared_data
    