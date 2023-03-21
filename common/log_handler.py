import logging 
import sys

LOG_OUTPUT = 'runs/latest.log'

class Logger():
    """
    Log everything in the system and write everything \
    into a log.txt file.
    This is a Singleton class.
    """
    __shared_instance = None

    def __new__(cls):
        if cls.__shared_instance is None:
            cls.log = cls.get_logger("delay_flight", LOG_OUTPUT)
            cls.__shared_instance = super().__new__(cls)
        
        return cls.__shared_instance
        
    @classmethod
    def get_logger(cls, name, path_log):
        file_handler = logging.FileHandler(filename=path_log)
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        handlers = [file_handler, stdout_handler]

        logging.basicConfig(
            level=logging.DEBUG, 
            format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
            handlers=handlers
        )

        return logging.getLogger(name)
