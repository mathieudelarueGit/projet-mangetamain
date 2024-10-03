import logging


def setup_logging():
    logging.basicConfig(
        filename="app.log",  # Logs will be written to 'app.log'
        filemode="a",  # Append mode: new logs will be added to the existing file
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log format: timestamp, log level, and message
        level=logging.DEBUG,  # Set the logging level to DEBUG to capture all events
    )
