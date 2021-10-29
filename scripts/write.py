import logging

from config import DB_ROOT


log_path = "{DB_ROOT}/{LOG_NAME}".format(DB_ROOT=DB_ROOT, LOG_NAME="logger.log")
logging.basicConfig(filename=log_path, level=logging.INFO)
logger = logging.getLogger(__name__)

class MultipleWriter:
  def write(self, msg: str, log_level: str) -> None:
    if msg:
      print(msg)
    if log_level == "info":
      logger.info(msg)
    elif log_level == "warning":
      logger.warning(msg)