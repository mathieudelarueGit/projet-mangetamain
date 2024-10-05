import unittest
from unittest.mock import patch
import pandas as pd
from algo_clustering import dataset_study, filtering_bio_recipes

class TestAlgoClustering(unittest.TestCase):
    """Test  for the functions in algo_clustering.py."""

    @patch('algo_clustering.load_data')
    def test_dataset_study(self, mock_load_data):
        """Test the dataset_study function by mocking the load_data function."""
        # Mock the DataFrame returned by load_data
        mock_df = pd.DataFrame({
            'Column1': [1, 2, 3],
            'Column2': [4, 5, 6]
        })
        mock_load_data.return_value = mock_df

        # Patch print to capture print statements
        with patch('builtins.print') as mocked_print:
            dataset_study('test.csv')

            # Verify that the correct columns and descriptions were printed
            mocked_print.assert_any_call("Column names:", mock_df.columns)
            mocked_print.assert_any_call(mock_df.describe())
            mocked_print.assert_any_call("Number of missing data:", 0)

    def test_filtering_bio_recipes(self):
        """Test filtering_bio_recipes to ensure it filters recipes correctly based on 'bio' or 'traditional' tags."""
        # Create a mock DataFrame for testing
        df = pd.DataFrame({
            'recipe_id': [1, 2, 3, 4],
            'tags': [['bio', 'healthy'], ['traditional'], ['vegan'], ['bio']]
        })

        # Call the filtering function
        filtered_df = filtering_bio_recipes(df)

        # Expected DataFrame after filtering
        expected_filtered = pd.DataFrame({
            'recipe_id': [1, 2, 4],
            'tags': [['bio', 'healthy'], ['traditional'], ['bio']]
        })

        # Compare the resulting DataFrame to the expected result
        pd.testing.assert_frame_equal(filtered_df, expected_filtered)

if __name__ == '__main__':
    unittest.main()
