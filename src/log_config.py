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
    Configures the global logging for the application, ensuring logs are
    written to files.

    - Creates a "src/logs" directory if it doesn't exist.
    - Sets up two separate log files: one for debug-level logs (DEBUG, INFO,
      WARNING) and one for error-level logs (ERROR, CRITICAL).
    - Adds the module name to log messages.

    Raises:
        OSError: If the log directory cannot be created.
    """

    # Define the directory where log files will be stored
    log_directory: str = "src/logs"

    # Check if the log directory exists, and if not, create it
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the logging level for the root logger

    # Add handlers only if none exist
    if not logger.hasHandlers():

        # Set up a file handler for debug-level logs (app_debug.log)
        debug_handler = logging.FileHandler(
            os.path.join(log_directory, "app_debug.log"), mode="a"
        )

        # Capture DEBUG, INFO, and WARNING logs
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        debug_handler.addFilter(MaxLevelFilter(logging.WARNING))

        # Set up a file handler for error-level logs (app_error.log)
        error_handler = logging.FileHandler(
            os.path.join(log_directory, "app_error.log"), mode="a"
        )

        # Capture only ERROR and CRITICAL logs
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )

        # Add both handlers to the root logger
        logger.addHandler(debug_handler)
        logger.addHandler(error_handler)
