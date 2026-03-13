import logging
import os
import sys


class AppLogger:
    _configured = False

    @classmethod
    def setup(cls, log_level: str, log_file: str):
        if cls._configured:
            return

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        cls._configured = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
