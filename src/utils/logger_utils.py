import logging

def setup_detailed_logger(log_file='detailed_log.log', log_level=logging.DEBUG):
    """
    Configures a detailed logger that includes the file name, line number, function name, and timestamp.

    :param log_file: The name of the file to write logs to (default: 'detailed_log.log').
    :param log_level: The minimum logging level (default: logging.DEBUG).
    :return: A configured logger object.
    """
    # Create the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)  # Set the minimum logging level

    # Detailed log format
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Usage of the logger function
logger = setup_detailed_logger(log_file='app_log.log', log_level=logging.DEBUG)