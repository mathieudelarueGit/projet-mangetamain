import logging
import os


class MaxLevelFilter(logging.Filter):
    """
    A logging filter that allows only messages below a certain level.
    """

    def __init__(self, max_level: int) -> None:
        """
        Initialize the filter with a maximum logging level.

        Parameters:
        ----------
        max_level : int
            The highest logging level this filter will allow.
        """
        self.max_level = max_level
        super().__init__()

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Determine whether a log record should be allowed.

        Parameters:
        ----------
        record : logging.LogRecord
            The log record to evaluate.

        Returns:
        -------
        bool
            True if the record level is below or equal to max_level, otherwise False.
        """
        return record.levelno <= self.max_level


def setup_logging() -> None:
    """
    Configure global logging for the application, ensuring logs are written to files.

    - Creates a "src/logs" directory if it doesn't exist.
    - Sets up two separate log files:
      1. `app_debug.log` for DEBUG, INFO, and WARNING logs.
      2. `app_error.log` for ERROR and CRITICAL logs.
    - Suppresses unnecessary debug logs from external libraries like Pillow.

    Raises:
    -------
    OSError
        If the log directory cannot be created.
    """
    log_directory: str = "src/logs"

    # Create the log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all logs at or above DEBUG level

    # Avoid adding handlers multiple times
    if not logger.hasHandlers():
        # Debug handler for detailed logs (DEBUG to WARNING)
        debug_handler = logging.FileHandler(
            os.path.join(log_directory, "app_debug.log"), mode="a"
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        debug_handler.addFilter(
            MaxLevelFilter(logging.WARNING)
        )  # Limit to DEBUG, INFO, and WARNING

        # Error handler for critical issues (ERROR and CRITICAL)
        error_handler = logging.FileHandler(
            os.path.join(log_directory, "app_error.log"), mode="a"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        # Add handlers to the root logger
        logger.addHandler(debug_handler)
        logger.addHandler(error_handler)

    # Suppress excessive debug logs from external libraries
    logging.getLogger("PIL").setLevel(logging.INFO)
