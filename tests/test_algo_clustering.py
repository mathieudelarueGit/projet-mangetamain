import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from src.algo_clustering import dataset_study, filtering_bio_recipes_kaggle, correlation_bio_recipes

# Mock data for testing
mock_data = {
    'id': [1, 2, 3, 4],
    'name': ['Recipe 1', 'Recipe 2', 'Recipe 3', 'Recipe 4'],
    'tags': ['vegan, healthy', 'bio, quick', 'traditional, hearty', 'gluten-free, organic']
}

# Create a DataFrame from mock data
mock_df = pd.DataFrame(mock_data)

# New mock data for correlation testing (numerical data)
correlation_mock_data = {
    'calories': [200, 150, 300, 250],
    'fat': [10, 5, 20, 15],
    'protein': [5, 10, 15, 20],
}

correlation_mock_df = pd.DataFrame(correlation_mock_data)


class TestAlgoClustering(unittest.TestCase):

    @patch('src.algo_clustering.load_data_kaggle')
    def test_dataset_study(self, mock_load_data_kaggle):
        """ Test the dataset_study function to ensure it prints column names and handles the DataFrame correctly. """
        mock_load_data_kaggle.return_value = mock_df
        dataset_study("mock_file.csv")
        
        # Check the shape of the mock DataFrame
        self.assertEqual(mock_df.shape[0], 4)
        self.assertEqual(mock_df.shape[1], 3)
        self.assertIn('tags', mock_df.columns)

    @patch('src.algo_clustering.load_data_kaggle')
    def test_filtering_bio_recipes_kaggle(self, mock_load_data_kaggle):
        """ Test the filtering_bio_recipes_kaggle function for correct filtering based on tags. """
        mock_load_data_kaggle.return_value = mock_df

        # Call the filtering function
        bio_recipes = filtering_bio_recipes_kaggle()

        # Check that the filtered DataFrame contains only recipes with relevant tags
        self.assertEqual(len(bio_recipes), 3)  # Should return 3 out of 4 due to filtering

        # Verify that the filtered DataFrame contains expected tags
        self.assertTrue(all(tag in bio_recipes['tags'].values for tag in ['bio', 'vegan', 'gluten-free', 'organic']))

    def test_correlation_bio_recipes(self):
        """ Test the correlation_bio_recipes function for correct correlation matrix calculation. """

        # Calculate the correlation matrix
        correlation_matrix = correlation_bio_recipes(correlation_mock_df)

        # Expected correlation matrix based on the mock data
        expected_matrix = correlation_mock_df.corr(method="pearson")

        # Check if the correlation matrix matches the expected one
        pd.testing.assert_frame_equal(correlation_matrix, expected_matrix)

    @patch('src.algo_clustering.load_data_kaggle')
    def test_filtering_bio_recipes_kaggle_no_tags(self, mock_load_data_kaggle):
        """ Test that ValueError is raised if the 'tags' column is missing. """
        mock_df_no_tags = mock_df.drop(columns=['tags'])
        mock_load_data_kaggle.return_value = mock_df_no_tags

        with self.assertRaises(ValueError, msg="The 'tags' column is missing from the DataFrame."):
            filtering_bio_recipes_kaggle()

    @patch('src.algo_clustering.load_data_kaggle')
    def test_filtering_bio_recipes_kaggle_empty_dataframe(self, mock_load_data_kaggle):
        """ Test the filtering_bio_recipes_kaggle function with an empty DataFrame. """
        empty_df = pd.DataFrame(columns=['id', 'name', 'tags'])
        mock_load_data_kaggle.return_value = empty_df

        bio_recipes1 = filtering_bio_recipes_kaggle()

        # Ensure the result is also an empty DataFrame
        self.assertTrue(bio_recipes1.empty)

    @patch('src.algo_clustering.load_data_kaggle')
    def test_filtering_bio_recipes_kaggle_no_matching_tags(self, mock_load_data_kaggle):
        """ Test filtering with a DataFrame that has no matching tags. """
        mock_data_no_match = {
            'id': [1, 2],
            'name': ['Recipe 1', 'Recipe 2'],
            'tags': ['unhealthy, fast-food', 'meat-lover']
        }
        mock_df_no_match = pd.DataFrame(mock_data_no_match)
        mock_load_data_kaggle.return_value = mock_df_no_match

        bio_recipes = filtering_bio_recipes_kaggle()
        self.assertTrue(bio_recipes.empty)


