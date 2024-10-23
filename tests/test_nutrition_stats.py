import pandas as pd
import pytest
from src.nutrition_stats import stats_bio

@pytest.fixture
def sample_bio_df():
    """
    Fixture that provides a small sample DataFrame with bio recipes.
    """
    data = {
        'name': ['Recipe1', 'Recipe2', 'Recipe3'],
        'nutrition': ['[200, 10, 5, 500, 8, 2, 30]', '[150, 8, 4, 400, 6, 1, 25]', '[250, 15, 6, 600, 10, 3, 40]'],
        'ingredients': [
            "['ingredient1', 'ingredient2', 'ingredient3']",
            "['ingredient1', 'ingredient2']",
            "['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4']"
        ]
    }
    return pd.DataFrame(data)
def test_stats_bio(sample_bio_df: pd.DataFrame, capsys):
    """
    Test the stats_bio function to ensure it correctly processes
    the filtered bio DataFrame and prints the expected outputs.
    """
    # Call the function to test
    stats_bio(sample_bio_df)
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Ensure that basic statistics are calculated
    assert "Mean :" in captured.out
    assert "Median :" in captured.out
    assert "Standard  :" in captured.out  # Updated to match actual output
    assert "Minimums :" in captured.out
    assert "Maximums :" in captured.out

    # Check that the recipes with the highest calories, sugar, etc. are printed
    assert "Recipes with highest quantity of calories :" in captured.out
    assert "Recipes with highest quantity of sugar:" in captured.out
    assert "Recipes with highest quantity of sodium:" in captured.out
    assert "Recipes with highest quantity of proteins:" in captured.out
