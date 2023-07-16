import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a logging handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Configure the message format
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(formatter)

    # Add the logging handler to the logger instance
    logger.addHandler(console_handler)

    return logger
