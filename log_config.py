import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

def setup_logger(name=__name__, level=None):
    env = os.getenv("ENV", "production").lower()

    if level is None:
        level = logging.INFO if env == "production" else logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    log_folder = f'logs/{env}'
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, f'{name}.log')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING if env == "production" else logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger