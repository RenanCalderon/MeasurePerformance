import logging, os
from logging.handlers import RotatingFileHandler

log_file = os.path.join(r"C:\Users\renan\Documents\Python\MusicSuite", 'app.log')


def setup_logger():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a handler to write to a rotating file
    file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    # Create a handler to display logs on the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a format for the logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Apply the format to the handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
