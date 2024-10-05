import unittest
from unittest.mock import patch, MagicMock
import logging
import os
from src.log_config import setup_logging, MaxLevelFilter


class TestLogConfig(unittest.TestCase):

    def setUp(self):
        # Reset any logging configuration before each test
        logger = logging.getLogger()
        logger.handlers = []  # Clear all handlers to simulate a fresh logger

    @patch("os.makedirs")
    @patch("os.path.exists")
    @patch("logging.FileHandler")
    @patch("logging.getLogger")
    def test_setup_logging_sets_correct_handlers(
        self, mock_getLogger, mock_FileHandler, mock_exists, mock_makedirs
    ):
        """
        Test that setup_logging sets the correct log handlers for DEBUG and ERROR.
        """
        # Mock log directory doesn't exist
        mock_exists.return_value = False

        # Mock the logger and file handler
        mock_logger = MagicMock()
        mock_logger.hasHandlers.return_value = (
            False  # Ensure that handlers are not reported as existing
        )

        # Simulate a real list for handlers, instead of the default MagicMock list
        mock_logger.handlers = []

        # Manually simulate addHandler behavior
        def add_handler_side_effect(handler):
            mock_logger.handlers.append(handler)

        mock_logger.addHandler.side_effect = add_handler_side_effect

        mock_getLogger.return_value = mock_logger
        mock_debug_handler = MagicMock()
        mock_error_handler = MagicMock()
        mock_FileHandler.side_effect = [mock_debug_handler, mock_error_handler]

        # Call setup_logging
        setup_logging()

        # Ensure the logger's addHandler method is called twice (once for each handler)
        self.assertEqual(mock_logger.addHandler.call_count, 2)

        # Ensure the handlers have correct logging levels
        mock_debug_handler.setLevel.assert_called_once_with(logging.DEBUG)
        mock_error_handler.setLevel.assert_called_once_with(logging.ERROR)

        # Ensure the formatter is set for both handlers
        mock_debug_handler.setFormatter.assert_called_once()
        mock_error_handler.setFormatter.assert_called_once()

        # Now, since we manually appended the handlers, we can check if they were added
        self.assertIn(mock_debug_handler, mock_logger.handlers)
        self.assertIn(mock_error_handler, mock_logger.handlers)

    def test_max_level_filter(self):
        """
        Test the MaxLevelFilter allows only messages below or equal to the specified max level.
        """
        max_level = logging.WARNING
        log_filter = MaxLevelFilter(max_level)

        # Create mock log records with different levels
        record_debug = MagicMock(levelno=logging.DEBUG)
        record_info = MagicMock(levelno=logging.INFO)
        record_warning = MagicMock(levelno=logging.WARNING)
        record_error = MagicMock(levelno=logging.ERROR)

        # Assertions for the filter behavior
        self.assertTrue(log_filter.filter(record_debug))
        self.assertTrue(log_filter.filter(record_info))
        self.assertTrue(log_filter.filter(record_warning))
        self.assertFalse(log_filter.filter(record_error))
