# Helper function to setup logging for the application.
# This file is part of NeveBit.

import logging
from threading import RLock
from PyQt6.QtCore import QObject, pyqtSignal


class QtHandler(logging.Handler, QObject):
    log_signal = pyqtSignal(str, str, str)

    def __init__(self):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.lock = RLock()
        self.full_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s\n')
        self.qt_formatter = logging.Formatter('%(message)s')  # Formatter without date/time
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        with self.lock:
            try:
                formatted_message = self.full_formatter.format(record)  # Get the formatted message
                unformatted_message = self.qt_formatter.format(record)  # Get the unformatted message
                level_name = record.levelname  # Get the level name
                self.log_signal.emit(formatted_message, unformatted_message, level_name)
            except Exception:
                self.handleError(record)


def setup_logging():
    logger = logging.getLogger('NeveBit')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # Console handler for everything at DEBUG level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Qt handler for GUI logging, set to DEBUG level
    qt_handler = QtHandler()
    qt_handler.setLevel(logging.DEBUG)
    logger.addHandler(qt_handler)

    return logger, qt_handler
