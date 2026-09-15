import logging
import sys
import os


def init_logger():
    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    root_app_logger = logging.getLogger("cascade")
    root_app_logger.setLevel(logging.DEBUG)

    root_app_logger.handlers.clear()
    root_app_logger.addHandler(ConsoleHandler(log_level, sys.stdout))


class ConsoleHandler(logging.StreamHandler):
    def __init__(self, log_level: str, stream):
        super().__init__(stream)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.setFormatter(formatter)
        self.setLevel(log_level)