import unittest
import pandas as pd
import numpy as np
from src.algo_clustering import dataset_study, filtering_bio_recipes_kaggle, correlation_bio_recipes

class TestRecipeFunctions(unittest.TestCase):

    def test_dataset_study(self):
        # Mock dataset
        mock_data = {
            'column1': [1, 2, 3],
            'column2': [4, 5, np.nan]
        }
        df = pd.DataFrame(mock_data)
        # Assuming you mock load_data function to return this dataframe
        df_result = dataset_study("mock_file.csv")
        
        self.assertEqual(df_result.isnull().sum().sum(), 1)  # Check if missing values are correct

    def test_filtering_bio_recipes_kaggle(self):
        # Mock the dataset and testing filtering
        mock_data = {
            'tags': ['bio, vegan', 'organic, healthy', 'traditional', 'random_tag'],
            'nutrition': ['1,2,3', '4,5,6', '7,8,9', '10,11,12']
        }
        df = pd.DataFrame(mock_data)
        
        # Assuming load_data_kaggle is mocked
        filtered_df = filtering_bio_recipes_kaggle(r'\b(bio|organic|traditional)\b')
        
        # Check that the filtering works correctly
        self.assertEqual(len(filtered_df), 3)
        self.assertIn('bio, vegan', filtered_df['tags'].values)

    def test_correlation_bio_recipes(self):
        # Mock numerical data for correlation
        mock_data = {
            'col1': [1, 2, 3, 4],
            'col2': [4, 5, 6, 7],
            'col3': [7, 8, 9, 10]
        }
        df = pd.DataFrame(mock_data)
        correlation_matrix = correlation_bio_recipes(df)
        
        # Check that correlation is computed correctly
        self.assertEqual(correlation_matrix.shape, (3, 3))
        self.assertAlmostEqual(correlation_matrix.loc['col1', 'col2'], 1.0)

if __name__ == '__main__':
    unittest.main()
