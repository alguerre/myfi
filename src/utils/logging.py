import logging


def get_logger(
    name: str,
) -> logging.Logger:
    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger
