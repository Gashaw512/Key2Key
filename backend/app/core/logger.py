# app/core/logger.py (Enhanced for Large Scale)

import logging
from logging.config import dictConfig
import sys
# NOTE: Requires: pip install python-json-logger
from pythonjsonlogger import jsonlogger

# Define the log format to include essential fields.
# We use custom fields like 'time', 'level', and 'message' for clarity.
JSON_LOG_FORMAT = (
    "%(time)s %(levelno)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)d "
    "%(message)s"
)

# 1. LOGGING CONFIGURATION DICTIONARY
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            # Use the JsonFormatter class
            "()": jsonlogger.JsonFormatter,
            "format": JSON_LOG_FORMAT,
        },
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "stdout": {
            # Direct output to standard output
            "class": "logging.StreamHandler",
            "formatter": "json_formatter", # Use the structured JSON formatter
            "stream": sys.stdout,
        },
    },
    "loggers": {
        # Root logger for all messages not caught by specific loggers
        "": {
            "handlers": ["stdout"],
            "level": "INFO",
            "propagate": False,
        },
        # Optional: Suppress noisy third-party libraries
        "uvicorn.access": {"handlers": ["stdout"], "level": "WARNING", "propagate": False},
        "sqlalchemy": {"handlers": ["stdout"], "level": "WARNING", "propagate": False},
    },
}

# 2. SETUP FUNCTION
def setup_logging():
    """Initializes the structured logging configuration."""
    dictConfig(LOGGING_CONFIG)

# 3. APPLICATION LOGGER
# We get the logger instance, but the setup function must be called in main.py
logger = logging.getLogger("key2key")

# Note: You can remove the dictConfig(LOGGING_CONFIG) call outside the function 
# to ensure it's controlled by the setup_logging() call in main.py's create_application().
# The provided code above is clean for external use.