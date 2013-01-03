#!/usr/bin/env python

"""
Copyright (c) 2006-2012 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import logging
import StringIO
import sys

from lib.core.enums import CUSTOM_LOGGING
from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

logging.addLevelName(CUSTOM_LOGGING.PAYLOAD, "PAYLOAD")
logging.addLevelName(CUSTOM_LOGGING.TRAFFIC_OUT, "TRAFFIC OUT")
logging.addLevelName(CUSTOM_LOGGING.TRAFFIC_IN, "TRAFFIC IN")

LOGGER = logging.getLogger("sqlmapLog")

LOGGER_HANDLER = None
try:
    import ctypes
    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
    LOGGER_HANDLER.level_map[logging.getLevelName("PAYLOAD")] = (None, "cyan", False)
    LOGGER_HANDLER.level_map[logging.getLevelName("TRAFFIC OUT")] = (None, "magenta", False)
    LOGGER_HANDLER.level_map[logging.getLevelName("TRAFFIC IN")] = ("magenta", None, False)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(logging.WARN)

# to handle logger with the RESTful API
LOGGER_OUTPUT = StringIO.StringIO()

# Logger recorder object, which keeps the log structure
class LogRecorder (logging.StreamHandler):
    """
    Logging handler class which only records CUSTOM_LOGGING.PAYLOAD entries
    to a global list.
    """
    loghist = []

    def emit(self, record):
        """
        Simply record the emitted events.
        """
        self.loghist.append ({'levelno':record.levelno,
                              'text':record.message % record.args if record.args else record.message,
                              'id':len(self.loghist)})

    def get_logs (self, start = None, end = None):
        """
        Retrieve the recorded events. Optional slicing via start/end.
        """
        return self.loghist[slice(start, end)]

LOG_RECORDER = LogRecorder()
LOGGER.addHandler(LOG_RECORDER)