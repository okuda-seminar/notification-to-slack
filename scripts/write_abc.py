import logging
from abc import ABCMeta, abstractmethod

from config import LOG_PATH


log_path = LOG_PATH.format(LOG_NAME="logger.log")
logging.basicConfig(filename=log_path, level=logging.INFO)
logger = logging.getLogger(__name__)

class MultipleWriter(metaclass=ABCMeta):
    @abstractmethod
    def logger(self, msg):
        pass

class info():
    def logger(self, msg):
        logger.info(msg)

class warning():
    def logger(self,msg):
        logger.warning(msg)

MultipleWriter.register(info)
MultipleWriter.register(warning)

if __name__ == "__main__":
    msg = "abc"
    subclass = MultipleWriter()
    subclass.logger(msg)
