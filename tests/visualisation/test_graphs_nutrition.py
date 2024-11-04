import pytest
import pandas as pd
import plotly.graph_objects as go
from src.visualisation.graphs_nutrition import plot_top_5_recipes_by_nutrition  


@pytest.fixture
def sample_combined_df():
    """Fixture to create a sample DataFrame for testing."""
    data = {
        'name': ['Recipe A', 'Recipe B', 'Recipe C', 'Recipe D', 'Recipe E', 'Recipe F'],
        'Calories': [500, 450, 600, 300, 200, 700],
        'Total Fat (g)': [20, 25, 30, 15, 10, 35],
        'Sugar (g)': [5, 10, 15, 5, 1, 25],
        'Sodium (mg)': [300, 400, 500, 200, 100, 600],
        'Protein (g)': [10, 20, 30, 15, 5, 25],
        'Saturated Fat (g)': [5, 7, 9, 2, 1, 10],
        'Carbohydrates (g)': [60, 50, 70, 40, 30, 80]
    }
    return pd.DataFrame(data)


def test_plot_top_5_recipes_by_nutrition(sample_combined_df):
    """Test the plot_top_5_recipes_by_nutrition function."""

    categories = [
    "Calories",
    "Total Fat (g)",
    "Sugar (g)",
    "Sodium (mg)",
    "Protein (g)",
    "Saturated Fat (g)",
    "Carbohydrates (g)",
    ]
    fig = plot_top_5_recipes_by_nutrition(sample_combined_df, categories)

    # Check if the figure is an instance of list
    assert isinstance(fig, dict) 

    # Check if the figure contains the expected number of traces (7 for each category)
    expected_traces = 7  # One trace per nutritional component
    assert len(fig) == expected_traces

    # Check if a figure is generated for each category
    assert len(fig) == len(categories)

    # Check if the figure for each category is an instance of go.Figure
    for category in categories:
        assert isinstance(fig[category], go.Figure)

    # Optionally, check if the layout title for one of the figures is correct
    assert fig["Calories"].layout.title.text == "Top 5 Recipes by Calories"
