import logging
import pathlib
from datetime import datetime

log_dirpath: pathlib.Path = pathlib.Path("./outputs")
log_dirpath.mkdir(parents=True, exist_ok=True)
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filepath = log_dirpath / f"{current_time}_logging.log"
file_handler = logging.FileHandler(filepath, mode="w")
file_logger_formatter = logging.Formatter(
    "[%(asctime)s][%(name)s][%(levelname)s] %(pathname)s - %(message)s"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_logger_formatter)


def get_my_logger(name: str) -> logging.Logger:
    """Get logger with console handler.

    Args:
        name (str): logger name

    Returns:
        logging.Logger: logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_logger_formatter = logging.Formatter(
            "[%(levelname)s] %(pathname)s - %(message)s"
        )
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_logger_formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger