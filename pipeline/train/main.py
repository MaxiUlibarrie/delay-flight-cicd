from pipeline.train.prepare import prepare_train_data
from pipeline.train.train import train

from common.log_handler import Logger

logger = Logger()

if __name__ == '__main__':
    logger.log.info("Preparing Data.")
    prepare_train_data()

    logger.log.info("Starting Training Process.")
    train()
