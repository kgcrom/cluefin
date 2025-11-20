"""Logging configuration for Cluefin CLI."""

import sys
from contextvars import ContextVar
from typing import Literal

from loguru import logger

# Context variable to store debug mode flag (thread-safe)
_debug_mode: ContextVar[bool] = ContextVar("debug_mode", default=False)


def set_debug_mode(enabled: bool) -> None:
    """Set the debug mode flag.

    Args:
        enabled: True to enable debug logging, False otherwise
    """
    _debug_mode.set(enabled)


def is_debug_mode() -> bool:
    """Check if debug mode is enabled.

    Returns:
        True if debug mode is enabled, False otherwise
    """
    return _debug_mode.get()


def setup_logging(debug: bool = False) -> None:
    """Configure loguru logger with appropriate level.

    Args:
        debug: True to enable DEBUG level logging, False for INFO level
    """
    # Remove default handler
    logger.remove()

    # Add new handler with appropriate log level
    log_level: Literal["DEBUG", "INFO"] = "DEBUG" if debug else "INFO"

    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # Set context variable
    set_debug_mode(debug)
