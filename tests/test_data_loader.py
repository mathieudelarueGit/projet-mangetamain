import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("os.listdir")
    @patch("src.data_loader.zipfile.ZipFile")
    def test_unzip_data_zipfile(self, mock_zipfile, mock_listdir, mock_makedirs, mock_exists):
        """
        Test that ZIP files are unzipped correctly and extracted files are returned.
        """
        mock_exists.return_value = False
        mock_listdir.return_value = ["file1.csv", "file2.csv"]

        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        file_name = "test.zip"
        result = self.data_loader.unzip_data(file_name)

        mock_zip.extractall.assert_called_once()
        mock_makedirs.assert_called_once_with("test_extracted")
        self.assertEqual(result, ["test_extracted/file1.csv", "test_extracted/file2.csv"])

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("os.listdir")
    @patch("src.data_loader.DataLoader.decompress_xz")
    def test_unzip_data_xzfile(self, mock_decompress_xz, mock_listdir, mock_makedirs, mock_exists):
        """
        Test that XZ files are decompressed correctly and the decompressed file is returned.
        """
        mock_exists.return_value = False
        mock_listdir.return_value = ["file1.csv"]
        mock_decompress_xz.return_value = "test_extracted/file1.csv"

        file_name = "test.xz"
        result = self.data_loader.unzip_data(file_name)

        mock_decompress_xz.assert_called_once_with(file_name, "test_extracted")
        mock_makedirs.assert_called_once_with("test_extracted")
        self.assertEqual(result, ["test_extracted/file1.csv"])

    @patch("pandas.read_csv")
    @patch("src.data_loader.DataLoader.unzip_data")
    def test_load_data_from_zip(self, mock_unzip_data, mock_read_csv):
        """
        Test that CSV files inside ZIP archives are loaded correctly.
        """
        mock_unzip_data.return_value = ["file1.csv"]
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        file_name = "test.zip"
        result = self.data_loader.load_data(file_name)

        mock_unzip_data.assert_called_once_with(file_name)
        mock_read_csv.assert_called_once_with("file1.csv")
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_csv")
    def test_load_data_from_csv(self, mock_read_csv):
        """
        Test that CSV files are loaded directly without unzipping.
        """
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        file_name = "test.csv"
        result = self.data_loader.load_data(file_name)

        mock_read_csv.assert_called_once_with(file_name)
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_pickle")
    def test_load_data_from_pickle(self, mock_read_pickle):
        """
        Test that Pickle files are loaded correctly.
        """
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_pickle.return_value = mock_df

        file_name = "test.pkl"
        result = self.data_loader.load_data(file_name)

        mock_read_pickle.assert_called_once_with(file_name)
        pd.testing.assert_frame_equal(result, mock_df)

    @patch("pandas.read_csv")
    @patch("src.data_loader.DataLoader.unzip_data")
    def test_load_data_from_xz(self, mock_unzip_data, mock_read_csv):
        """
        Test that CSV files inside XZ archives are loaded correctly.
        """
        mock_unzip_data.return_value = ["test_extracted/file1.csv"]
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df

        file_name = "test.xz"
        result = self.data_loader.load_data(file_name)

        mock_unzip_data.assert_called_once_with(file_name)
        mock_read_csv.assert_called_once_with("test_extracted/file1.csv")
        pd.testing.assert_frame_equal(result, mock_df)

    def test_load_data_unsupported_file_type(self):
        """
        Test that an unsupported file type raises the correct exception.
        """
        file_name = "test.txt"
        with self.assertRaises(ValueError) as context:
            self.data_loader.load_data(file_name)
        self.assertEqual(str(context.exception), f"Unsupported file type: {file_name}")
    
    @patch("os.path.exists")
    @patch("os.makedirs")
    def test_unzip_data_unsupported_file_type(self, mock_makedirs, mock_exists):
        """
        Test that an unsupported file type raises a ValueError in unzip_data.
        """
        mock_exists.return_value = False
        file_name = "test.unsupported"

        with self.assertRaises(ValueError) as context:
            self.data_loader.unzip_data(file_name)

        self.assertEqual(str(context.exception), f"Unsupported file type for {file_name}")

