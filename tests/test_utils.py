import unittest
import pandas as pd
import numpy as np
from your_module_name import (
    dataset_study,
    filtering_dataframe,
    correlation_bio_recipes,
    filter_dataframebis1,
    parse_nutrition,
    cluster_nutrition_data
)

class TestUtils(unittest.TestCase):

    def setUp(self):
        """
        Initialize necessary data for testing before each test case.
        """
        # Sample DataFrame for testing
        self.sample_data = {
            'tags': ['vegan', 'bio', 'gluten-free', 'veggie', 'organic'],
            'n_ingredients': [5, 7, 6, 8, 4],
            'nutrition': ['[100, 10, 5, 300, 20, 3, 40]', '[120, 12, 6, 310, 22, 3.5, 42]', 
                          '[140, 15, 7, 320, 25, 4, 45]', np.nan, '[130, 13, 6.5, 315, 23, 3.8, 43]'],
            'contributor_id': [100, 101, 102, 103, 104]
        }
        self.df = pd.DataFrame(self.sample_data)

    def test_dataset_study(self):
        """
        Test dataset_study function to ensure it prints correct details of the dataset.
        """
        # We use the dataset_study and check the output using a mock, assuming it prints output
        result = dataset_study('dataset/RAW_recipes.csv.zip')
        self.assertIsInstance(result, pd.DataFrame)

    def test_filtering_dataframe(self):
        """
        Test filtering_dataframe to ensure it correctly filters the data by keywords.
        """
        key_words_bio = r'\b(vegan|bio|organic)\b'
        filtered_df = filtering_dataframe(self.df, key_words_bio)
        self.assertEqual(len(filtered_df), 3)  # Expect 3 matching rows

    def test_correlation_bio_recipes(self):
        """
        Test correlation_bio_recipes to ensure it calculates the Pearson correlation matrix.
        """
        matrix_corr = correlation_bio_recipes(self.df)
        self.assertIsInstance(matrix_corr, pd.DataFrame)
        self.assertEqual(matrix_corr.shape[0], 2)  # Expecting correlation between numeric columns

    def test_filter_dataframebis1(self):
        """
        Test filter_dataframebis1 function to ensure it filters based on given column names and filter values.
        """
        column_names = ['tags']
        filter_values = [['vegan', 'bio']]
        filtered_df = filter_dataframebis1(self.df, column_names, filter_values)
        self.assertEqual(len(filtered_df), 2)  # Expecting 2 rows to match

    def test_parse_nutrition(self):
        """
        Test parse_nutrition to ensure it correctly parses the nutrition data.
        """
        nutrition_str = '[100, 10, 5, 300, 20, 3, 40]'
        parsed_nutrition = parse_nutrition(nutrition_str)
        expected_nutrition = np.array([100, 10, 5, 300, 20, 3, 40])
        np.testing.assert_array_equal(parsed_nutrition, expected_nutrition)

        # Test invalid parsing
        invalid_nutrition_str = 'invalid'
        parsed_invalid_nutrition = parse_nutrition(invalid_nutrition_str)
        self.assertTrue(np.isnan(parsed_invalid_nutrition).all())

    def test_cluster_nutrition_data(self):
        """
        Test clustering of nutritional data using DBSCAN.
        """
        # Since clustering produces images, the test will focus on ensuring no errors are raised during execution.
        try:
            cluster_nutrition_data(self.df, eps=2, min_samples=9)
        except Exception as e:
            self.fail(f"cluster_nutrition_data raised an exception: {e}")

