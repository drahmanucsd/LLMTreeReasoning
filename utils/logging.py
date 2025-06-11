import logging
import sys
from config import LOG_LEVEL, LOG_FILE

# Convert log level string to logging module level
level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

# Create root logger
logger = logging.getLogger()
logger.setLevel(level)

# Formatter for all handlers
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(level)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
try:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"Could not set up file handler at {LOG_FILE}: {e}")


def log_debug(message: str, **kwargs):
    """Log a debug-level message with optional structured metadata."""
    if kwargs:
        message = f"{message} | {kwargs}"
    logger.debug(message)


def log_info(message: str, **kwargs):
    """Log an info-level message with optional structured metadata."""
    if kwargs:
        message = f"{message} | {kwargs}"
    logger.info(message)


def log_warning(message: str, **kwargs):
    """Log a warning-level message with optional structured metadata."""
    if kwargs:
        message = f"{message} | {kwargs}"
    logger.warning(message)


def log_error(message: str, **kwargs):
    """Log an error-level message with optional structured metadata."""
    if kwargs:
        message = f"{message} | {kwargs}"
    logger.error(message)


def log_metrics(metric_name: str, value, **tags):
    """
    Log a metric for monitoring purposes.

    Example:
        log_metrics('explore_latency', 1.23, branch='auth_module')
    """
    tag_str = ','.join(f"{k}={v}" for k, v in tags.items()) if tags else ''
    logger.info(f"METRIC {metric_name}={value} {tag_str}")
