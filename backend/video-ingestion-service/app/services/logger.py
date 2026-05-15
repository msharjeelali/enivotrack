import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class AppLogger:
    _configured = False

    @classmethod
    def setup(cls, log_level: str, log_file: str) -> None:
        if cls._configured:
            return

        try:
            level = getattr(logging, log_level.upper(), logging.INFO)

            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            formatter = logging.Formatter(LOG_FORMAT)
            root_logger = logging.getLogger()
            root_logger.setLevel(level)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

            file_handler = RotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

            cls._configured = True

        except Exception as e:
            logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
            logging.error(f"Logger setup failed: {e}", exc_info=True)

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
