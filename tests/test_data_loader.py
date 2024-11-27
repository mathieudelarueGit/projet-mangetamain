import unittest
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
        self.test_csv_file = "test_file.csv"
        self.test_zip_file = "test_file.zip"

        # Create a sample CSV file
        self.sample_data = pd.DataFrame({
            "nutrition": ["[1.0, 2.0, 3.0]", "[4.0, 5.0, 6.0]"],
            "ingredient_PP": ["['salt', 'sugar']", "['flour', 'water']"],
        })
        self.sample_data.to_csv(self.test_csv_file, index=False)

        # Create a ZIP file containing the CSV
        with zipfile.ZipFile(self.test_zip_file, "w") as zipf:
            zipf.write(self.test_csv_file)

    def tearDown(self):
        """
        Clean up resources after each test.
        """
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)
        if os.path.exists(self.test_zip_file):
            os.remove(self.test_zip_file)
        extracted_dir = os.path.splitext(self.test_zip_file)[0] + "_extracted"
        if os.path.exists(extracted_dir):
            for file in os.listdir(extracted_dir):
                os.remove(os.path.join(extracted_dir, file))
            os.rmdir(extracted_dir)

    def test_unzip_data(self):
        """
        Test the unzip_data method.
        """
        extracted_files = self.data_loader.unzip_data(self.test_zip_file)
        self.assertTrue(os.path.exists(extracted_files[0]))
        self.assertTrue(extracted_files[0].endswith(".csv"))

    def test_load_data_csv(self):
        """
        Test the load_data method with a CSV file.
        """
        df = self.data_loader.load_data(self.test_csv_file)
        pd.testing.assert_frame_equal(df, self.sample_data)

    def test_load_data_zip(self):
        """
        Test the load_data method with a ZIP file.
        """
        df = self.data_loader.load_data(self.test_zip_file)
        pd.testing.assert_frame_equal(df, self.sample_data)

    def test_load_and_parse_data(self):
        """
        Test the load_and_parse_data method.
        """
        df, ingredient_list = self.data_loader.load_and_parse_data(self.test_csv_file)

        # Test the parsed DataFrame
        expected_nutrition = [
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
        ]
        expected_ingredients = [
            ["salt", "sugar"],
            ["flour", "water"],
        ]
        self.assertEqual(df["nutrition"].tolist(), expected_nutrition)
        self.assertEqual(df["ingredient_PP"].tolist(), expected_ingredients)

        # Test the MTM score column
        self.assertIn("mtm_score", df.columns)

        # Test the ingredient list
        expected_ingredient_set = {"salt", "sugar", "flour", "water"}
        self.assertEqual(set(ingredient_list), expected_ingredient_set)

if __name__ == "__main__":
    unittest.main()
