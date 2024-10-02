import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import pandas as pd
from src.data_loader import unzip_data, load_data


class TestDataLoader(unittest.TestCase):

    @patch("src.data_loader.zipfile.ZipFile")
    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("os.listdir")
    def test_unzip_data(self, mock_listdir, mock_makedirs, mock_exists, mock_zipfile):
        # Mock the file existence check and list of extracted files
        mock_exists.return_value = False
        mock_listdir.return_value = ["file1.csv", "file2.csv"]

        # Create a mock zip file object
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Call the function
        file_name = "test.zip"
        result = unzip_data(file_name)

        # Assertions
        mock_zip.extractall.assert_called_once()
        mock_makedirs.assert_called_once_with("test_extracted")
        self.assertEqual(
            result, ["test_extracted/file1.csv", "test_extracted/file2.csv"]
        )

    @patch("src.data_loader.unzip_data")
    @patch("pandas.read_csv")
    def test_load_data_from_zip(self, mock_read_csv, mock_unzip_data):
        # Mock the unzip function and pandas read_csv
        mock_unzip_data.return_value = ["file1.csv"]
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        # Call the function
        file_name = "test.zip"
        result = load_data(file_name)

        # Assertions
        mock_unzip_data.assert_called_once_with(file_name)
        mock_read_csv.assert_called_once_with("file1.csv")
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_csv")
    def test_load_data_from_csv(self, mock_read_csv):
        # Mock pandas read_csv
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        # Call the function
        file_name = "test.csv"
        result = load_data(file_name)

        # Assertions
        mock_read_csv.assert_called_once_with(file_name)
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_pickle")
    def test_load_data_from_pickle(self, mock_read_pickle):
        # Mock pandas read_pickle
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_pickle.return_value = mock_df

        # Call the function
        file_name = "test.pkl"
        result = load_data(file_name)

        # Assertions
        mock_read_pickle.assert_called_once_with(file_name)
        pd.testing.assert_frame_equal(result, mock_df)

    def test_load_data_unsupported_file_type(self):
        # Call the function with an unsupported file type
        file_name = "test.txt"

        # Assertions
        with self.assertRaises(ValueError) as context:
            load_data(file_name)
        self.assertEqual(str(context.exception), f"Unsupported file type: {file_name}")
