from loguru import logger
import sys
from ..config.settings import LOG_FILE, LOG_LEVEL


# Logger configuration
def setup_logger():
    """
    Configure the logger with appropriate settings for our project.
    Writes the logs both to the console and to a file.
    """
    # We remove the default handler
    logger.remove()

    # We add a handler for the console
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=LOG_LEVEL,
        colorize=True
    )

    # We add a file handler
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=LOG_LEVEL,
        rotation="10 MB",  # New file every 10MB
        retention="1 week"  # Keep logs for 1 week
    )

    return logger


# We create a global instance of the logger
app_logger = setup_logger()


# Helper functions for frequently used logs
def log_start_process(process_name: str):
    """Process start log"""
    app_logger.info(f"A process is starting: {process_name}")


def log_end_process(process_name: str):
    """Process completion log"""
    app_logger.info(f"Ending a process: {process_name}")


def log_error(error: Exception, process_name: str = None):
    """Error log with details"""
    if process_name:
        app_logger.error(f"Error in process {process_name}: {str(error)}")
    else:
        app_logger.error(f"Error: {str(error)}")