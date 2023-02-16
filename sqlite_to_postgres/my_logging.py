import logging
from pathlib import Path


BASE_DIR = Path(__name__).resolve().parent.parent

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(BASE_DIR / 'information.log', mode='w')

file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s %(message)s')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info("Logger initialized")
