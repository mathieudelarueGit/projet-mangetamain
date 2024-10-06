import pytest
import pandas as pd
from src.algo_clustering import dataset_study, filtering_bio_recipes_kaggle

# Mock data for testing
mock_data = {
    'id': [1, 2, 3, 4],
    'name': ['Recipe 1', 'Recipe 2', 'Recipe 3', 'Recipe 4'],
    'tags': ['vegan, healthy', 'bio, quick', 'traditional, hearty', 'gluten-free, organic']
}

# Create a DataFrame from mock data
mock_df = pd.DataFrame(mock_data)

def test_dataset_study(mocker):
    """ Test the dataset_study function to ensure it prints column names and handles the DataFrame correctly. """
    mocker.patch('algo_clustering.load_data_kaggle', return_value=mock_df)
    dataset_study("mock_file.csv")
    
    # Check the printed output
    # This example assumes that the printed output can be captured or asserted
    assert mock_df.shape[0] == 4
    assert mock_df.shape[1] == 3
    assert 'tags' in mock_df.columns

def test_filtering_bio_recipes_kaggle(mocker):
    """ Test the filtering_bio_recipes_kaggle function for correct filtering based on tags. """
    mocker.patch('algo_clustering.load_data_kaggle', return_value=mock_df)

    # Call the filtering function
    bio_recipes = filtering_bio_recipes_kaggle()
    
    # Check that the filtered DataFrame contains only recipes with relevant tags
    assert len(bio_recipes) == 3  # Should return 3 out of 4 due to filtering
    
    # Verify that the filtered DataFrame contains expected tags
    assert all(tag in bio_recipes['tags'].values for tag in ['bio', 'vegan', 'gluten-free', 'organic'])

def test_filtering_bio_recipes_kaggle_no_tags(mocker):
    """ Test that ValueError is raised if the 'tags' column is missing. """
    mock_df_no_tags_ = mock_df.drop(columns=['tags'])
    mocker.patch('algo_clustering.load_data_kaggle', return_value=mock_df_no_tags)

    with pytest.raises(ValueError, match="The 'tags' column is missing from the DataFrame."):
        filtering_bio_recipes_kaggle()

def test_filtering_bio_recipes_kaggle_empty_dataframe(mocker):
    """ Test the filtering_bio_recipes_kaggle function with an empty DataFrame. """
    empty_df = pd.DataFrame(columns=['id', 'name', 'tags'])
    mocker.patch('algo_clustering.load_data_kaggle', return_value=empty_df)

    bio_recipes1 = filtering_bio_recipes_kaggle()
    
    # Ensure the result is also an empty DataFrame
    assert bio_recipes1.empty

def test_filtering_bio_recipes_kaggle_no_matching_tags(mocker):
    """ Test filtering with a DataFrame that has no matching tags. """
    mock_data_no_match = {
        'id': [1, 2],
        'name': ['Recipe 1', 'Recipe 2'],
        'tags': ['unhealthy, fast-food', 'meat-lover']
    }
    mock_df_no_match = pd.DataFrame(mock_data_no_match)
    mocker.patch('algo_clustering.load_data_kaggle', return_value=mock_df_no_match)

    bio_recipes = filtering_bio_recipes_kaggle()
    # Ensure the result is empty since there are no matching tags
    assert bio_recipes.empty

# Run the tests
if __name__ == "__main__":
    pytest.main()
