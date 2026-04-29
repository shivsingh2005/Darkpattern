"""
Structured logging configuration with loguru integration.
"""

import logging
import logging.config
import sys
from typing import Optional

from backend.app.core.config import settings


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    log_file: Optional[str] = None,
) -> None:
    """
    Configure structured logging with loguru.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Log format string
        log_file: Optional log file path
    """
    try:
        from loguru import logger as loguru_logger

        # Remove default handler
        loguru_logger.remove()

        # Add console handler
        loguru_logger.add(
            sys.stderr,
            level=level,
            format=format_string
            or "<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        )

        # Add file handler if specified
        if log_file:
            loguru_logger.add(
                log_file,
                level=level,
                format=format_string
                or "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
                rotation="500 MB",
                retention="7 days",
            )
    except ImportError:
        # Fallback to standard logging if loguru not available
        setup_standard_logging(level, log_file)


def setup_standard_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
) -> None:
    """
    Configure standard Python logging as fallback.

    Args:
        level: Logging level
        log_file: Optional log file path
    """
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "detailed",
                "stream": "ext://sys.stderr",
            },
        },
        "root": {
            "level": level,
            "handlers": ["console"],
        },
    }

    if log_file:
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "detailed",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 10,
        }
        logging_config["root"]["handlers"].append("file")

    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Initialize logging on module import
setup_logging(
    level=settings.logging.level,
    log_file=settings.logging.file,
)

logger = get_logger(__name__)
