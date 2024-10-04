import logging
import os


class MaxLevelFilter(logging.Filter):
    """
    A logging filter that allows only messages below a certain level.
    """

    def __init__(self, max_level: int) -> None:
        self.max_level = max_level
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= self.max_level


def setup_logging() -> None:
    """
    Configures the global logging for the application, ensuring logs are written to files.
    - Creates a "src/logs" directory if it doesn't exist.
    - Sets up two separate log files: one for debug-level logs (DEBUG, INFO, WARNING)
      and one for error-level logs (ERROR, CRITICAL).
    - Adds the module name to log messages.
    """

    # Define the directory where log files will be stored
    log_directory: str = "src/logs"

    # Check if the log directory exists, and if not, create it
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure the root logger with the basic settings (but without any handlers)
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level to capture DEBUG and higher
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Include module name
        datefmt="-%d-%m%Y %H:%M:%S",  # Timestamp format
    )

    # Set up a file handler for debug-level logs (app_debug.log)
    debug_handler: logging.FileHandler = logging.FileHandler(
        os.path.join(log_directory, "app_debug.log")
    )
    debug_handler.setLevel(logging.DEBUG)  # Capture DEBUG, INFO, and WARNING logs
    debug_formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Include module name
    )
    debug_handler.setFormatter(debug_formatter)

    # Add a filter to the debug_handler to exclude ERROR and CRITICAL logs
    debug_handler.addFilter(MaxLevelFilter(logging.WARNING))

    # Set up a file handler for error-level logs (app_error.log)
    error_handler: logging.FileHandler = logging.FileHandler(
        os.path.join(log_directory, "app_error.log")
    )
    error_handler.setLevel(logging.ERROR)  # Capture only ERROR and CRITICAL logs
    error_formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Include module name
    )
    error_handler.setFormatter(error_formatter)

    # Get the root logger
    logger: logging.Logger = logging.getLogger()

    # Clear existing handlers to avoid duplicate logs if setup_logging is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add both the debug and error handlers to the root logger
    logger.addHandler(
        debug_handler
    )  # Only DEBUG, INFO, WARNING will go to app_debug.log
    logger.addHandler(error_handler)  # Only ERROR and CRITICAL will go to app_error.log
