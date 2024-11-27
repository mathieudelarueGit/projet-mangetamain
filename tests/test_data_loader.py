import unittest
from unittest.mock import patch, MagicMock
import os
import zipfile
import pandas as pd
from src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """
        Set up resources for each test.
        """
        self.data_loader = DataLoader()
        self.sample_data = pd.DataFrame({
            "nutrition": ["[1.0, 2.0, 3.0]", "[4.0, 5.0, 6.0]"],
            "ingredient_PP": ["['salt', 'sugar']", "['flour', 'water']"],
        })

    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("os.listdir")
    @patch("src.data_loader.zipfile.ZipFile")
    def test_unzip_data(self, mock_zipfile, mock_listdir, mock_makedirs, mock_exists):
        """
        Test the unzip_data method.
        """
        # Mock behaviors
        mock_exists.return_value = False
        mock_listdir.return_value = ["file1.csv", "file2.csv"]
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Test unzip_data
        file_name = "test.zip"
        extracted_files = self.data_loader.unzip_data(file_name)

        # Verify behaviors
        mock_makedirs.assert_called_once_with("test_extracted")
        mock_zip.extractall.assert_called_once_with("test_extracted")
        self.assertEqual(extracted_files, ["test_extracted/file1.csv", "test_extracted/file2.csv"])
        mock_exists.assert_called_once_with("test_extracted")

    @patch("pandas.read_csv")
    def test_load_data_csv(self, mock_read_csv):
        """
        Test the load_data method with a CSV file.
        """
        # Mock pandas.read_csv
        mock_read_csv.return_value = self.sample_data

        # Test load_data
        file_name = "test.csv"
        df = self.data_loader.load_data(file_name)

        # Assertions
        pd.testing.assert_frame_equal(df, self.sample_data)
        mock_read_csv.assert_called_once_with(file_name)

    @patch("src.data_loader.DataLoader.unzip_data")
    @patch("pandas.read_csv")
    def test_load_data_zip(self, mock_read_csv, mock_unzip_data):
        """
        Test the load_data method with a ZIP file.
        """
        # Mock behaviors
        mock_unzip_data.return_value = ["test_extracted/file1.csv"]
        mock_read_csv.return_value = self.sample_data

        # Test load_data
        file_name = "test.zip"
        df = self.data_loader.load_data(file_name)

        # Assertions
        pd.testing.assert_frame_equal(df, self.sample_data)
        mock_unzip_data.assert_called_once_with(file_name)
        mock_read_csv.assert_called_once_with("test_extracted/file1.csv")

    @patch("src.data_loader.DataLoader.load_data")
    def test_load_and_parse_data(self, mock_load_data):
        """
        Test the load_and_parse_data method.
        """
        # Mock load_data behavior
        mock_load_data.return_value = self.sample_data

        # Test load_and_parse_data
        file_name = "test.csv"
        df, ingredient_list = self.data_loader.load_and_parse_data(file_name)

        # Expected results
        expected_nutrition = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]
        expected_ingredients = [
            ["salt", "sugar"],
            ["flour", "water"],
        ]

        # Assertions
        self.assertEqual(df["nutrition"].tolist(), expected_nutrition)
        self.assertEqual(df["ingredient_PP"].tolist(), expected_ingredients)
        self.assertIn("mtm_score", df.columns)
        expected_ingredient_set = {"salt", "sugar", "flour", "water"}
        self.assertEqual(set(ingredient_list), expected_ingredient_set)


if __name__ == "__main__":
    unittest.main()
