import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.utils import dataset_study, filtering_dataframe, filter_dataframebis1  # replace 'your_module' with the actual module name
print(pd.__version__)
class TestRecipeFunctions(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = {
            'tags': ['vegan', 'organic', 'traditional', 'gluten-free'],
            'n_ingredients': [5, 7, 10, 4],
            'minutes': [30, 60, 90, 15]
        }
        self.df = pd.DataFrame(self.data)

    @patch('builtins.print')
    def test_dataset_study(self, mock_print):
        # Call the dataset_study function
        dataset_study(self.df)

        # Check that print was called for column names and description
        self.assertIn("Column names:", mock_print.call_args_list[0][0][0])
        self.assertIn("n_ingredients", mock_print.call_args_list[0][0][0])
        self.assertIn("Number of missing data:", mock_print.call_args_list[2][0][0])

    def test_filtering_dataframe(self):
        # Define a keyword pattern
        key_words_bio = r'\b(organic|vegan)\b'
        
        # Call filtering_dataframe function
        filtered_df = filtering_dataframe(self.df, key_words_bio)

        # Check the filtered DataFrame
        self.assertEqual(len(filtered_df), 2)  # Expecting 2 rows
        self.assertTrue(filtered_df['tags'].isin(['organic', 'vegan']).all())

    def test_filter_dataframebis1(self):
        # Define column names and filter values
        column_names = ['tags', 'n_ingredients']
        filter_values = [['organic', 'vegan'], [5, 7]]

        # Call filter_dataframebis1 function
        filtered_df = filter_dataframebis1(self.df, column_names, filter_values)

        # Check the filtered DataFrame
        self.assertEqual(len(filtered_df), 2)  # Expecting 2 rows
        self.assertTrue(filtered_df['tags'].isin(['organic', 'vegan']).all())

        # Check filtering with incorrect column name
        with self.assertRaises(KeyError):
            filter_dataframebis1(self.df, ['invalid_column'], [1])

        # Check filtering with mismatched lengths
        with self.assertRaises(ValueError):
            filter_dataframebis1(self.df, ['tags'], ['organic', 'vegan'])

if __name__ == '__main__':
    unittest.main()
