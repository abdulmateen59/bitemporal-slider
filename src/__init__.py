import datetime
import logging
import os
from enum import Enum

__all__ = ["ColumnName", "logger"]


class ColumnName(Enum):
    SYSTEM = "system"
    VALID = "valid"
    DATA = "data"


class MyLogger:

    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._logger is None:
            print("\n", "*" * 10, "Logger instance initialized", "*" * 10, "\n")
            cls._logger = super().__new__(cls, *args, **kwargs)
            cls._logger = logging.getLogger("crumbs")
            cls._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s  [%(levelname)s | %(filename)s:%(lineno)s] ->  %(message)s")

            now = datetime.datetime.now()
            dirname = "./log"

            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            fileHandler = logging.FileHandler(
                f"{dirname}/log_" + now.strftime("%Y-%m-%d") + ".log")

            streamHandler = logging.StreamHandler()

            fileHandler.setFormatter(formatter)
            streamHandler.setFormatter(formatter)

            cls._logger.addHandler(fileHandler)
            cls._logger.addHandler(streamHandler)

        return cls._logger


logger = MyLogger()
