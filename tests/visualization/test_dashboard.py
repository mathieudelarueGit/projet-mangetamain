import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import streamlit as st
from src.visualization.dashboard import RecipeVisualizer

class TestRecipeVisualizer(unittest.TestCase):
    """
    Unit tests for the RecipeVisualizer class.
    """

    def setUp(self):
        """
        Set up sample data for testing.
        """
        self.recipes_df = pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Recipe A", "Recipe B", "Recipe C"],
            "ingredient_PP": [
                ["chicken", "salt", "pepper"],
                ["beef", "onion", "garlic"],
                ["tofu", "soy sauce", "ginger"]
            ],
            "nutrition": [
                [400, 20, 10, 3, 15, 5, 50],
                [300, 15, 8, 2, 10, 4, 30],
                [500, 25, 12, 4, 20, 6, 70],
            ],
            "mtm_score": [75, 60, 85],
            "avg_date": [1.5, 6, 11.2],
            "steps": ['["Step 1", "Step 2"]', '["Step 1", "Step 2"]', '["Step 1", "Step 2"]']
        })

        self.interactions_df = pd.DataFrame({
            "recipe_id": [1, 1, 2, 3, 3, 3],
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06"],
        })

        self.visualizer = RecipeVisualizer(self.recipes_df, self.interactions_df)

    @patch("streamlit.markdown")
    @patch("streamlit.write")
    def test_render_no_recipes_suggestions(self, mock_write, mock_markdown):
        """
        Test the render_no_recipes_suggestions method.
        """
        selected_ingredients = ["chicken", "salt"]
        with patch("streamlit.session_state", {}):
            self.visualizer.render_no_recipes_suggestions(selected_ingredients)

            # Check if suggestions header was written
            mock_markdown.assert_any_call(
                "<h2 style='color:#FF6347;'>🔍 Suggestions Based on Your Ingredients</h2>",
                unsafe_allow_html=True
            )

            # Check if the message was written
            mock_write.assert_any_call(
                "We didn't find any recipes that match your criteria. "
                "Here are some suggestions based on your selected ingredients. "
                "Consider adding the missing ingredients!"
            )

            # Check if individual recipes were displayed
            self.assertTrue(mock_write.called)

@patch("src.visualization.dashboard.RecipeVisualizer.render_navigation")
@patch("src.visualization.dashboard.RecipeVisualizer.render_pie_chart")
@patch("src.visualization.dashboard.RecipeVisualizer.render_score_chart")
def test_render_navigation(self, mock_render_score_chart, mock_render_pie_chart, mock_render_navigation):
    """
    Test the render_navigation method.
    """
    # Mock DataFrame setup (exemple de recettes)
    recipes_data = {
        'name': ['Recipe A', 'Recipe B', 'Recipe C', 'Recipe D'],
        'id': [1, 2, 3, 4],
        'nutrition': [[52.0, 0.0, 6.5, 0.0, 1.0, 0.0, 12.0], [387.34, 13.26, 5.0, 0.046, 7.0, 1.6, 60.0], [100, 20, 10, 5, 3, 1, 20], [200, 10, 15, 2, 8, 2, 30]],  # Nutrition mockée
        'ingredient_PP': [['squash', 'seasoning'], ['cheese', 'potato'], ['chicken', 'rice'], ['beef', 'carrot']],
        'avg_date': [5.0, 10.0, 3.0, 8.0],  # Dates mockées
        'steps': ['["Step1", "Step2"]', '["Step1", "Step2"]', '["Step1", "Step2"]', '["Step1", "Step2"]'],
        'mtm_score': [50, 60, 80, 70]
    }
    mock_recipes_df = pd.DataFrame(recipes_data)

    # Initialisation de st.session_state avant le test
    if "current_recipe_index" not in st.session_state:
        st.session_state["current_recipe_index"] = 0  # Assure-toi que l'index est initialisé

    # Mock de render_navigation pour renvoyer la recette actuelle correctement
    mock_render_navigation.return_value = (mock_recipes_df, mock_recipes_df.iloc[2])  # Simule "Recipe C" comme recette actuelle

    # Initialisation de RecipeVisualizer
    visualizer = RecipeVisualizer(mock_recipes_df, pd.DataFrame())

    # Appel de render_navigation
    filtered_recipes, current_recipe = visualizer.render_navigation(mock_recipes_df)

    # Assertion que le nom de la recette est "Recipe C"
    self.assertEqual(current_recipe["name"], "Recipe C")

    # Vérifier que les autres méthodes sont appelées
    mock_render_pie_chart.assert_called_once_with(current_recipe)
    mock_render_score_chart.assert_called_once_with(current_recipe)

    @patch("streamlit.plotly_chart")
    def test_render_pie_chart(self, mock_plotly_chart):
        """
        Test the render_pie_chart method.
        """
        selected_recipe = self.recipes_df.iloc[0]
        self.visualizer.render_pie_chart(selected_recipe)

        # Assert that plotly_chart was called once
        mock_plotly_chart.assert_called_once()

    @patch("streamlit.plotly_chart")
    def test_render_popularity_chart(self, mock_plotly_chart):
        """
        Test the render_popularity_chart method.
        """
        selected_recipe = self.recipes_df.iloc[0]
        self.visualizer.render_popularity_chart(selected_recipe)

        # Assert that plotly_chart was called once
        mock_plotly_chart.assert_called_once()

    @patch("streamlit.plotly_chart")
    def test_render_score_chart(self, mock_plotly_chart):
        """
        Test the render_score_chart method.
        """
        selected_recipe = self.recipes_df.iloc[0]
        self.visualizer.render_score_chart(selected_recipe)

        # Assert that plotly_chart was called once
        mock_plotly_chart.assert_called_once()

@patch("src.visualization.dashboard.RecipeVisualizer.render_navigation")
@patch("src.visualization.dashboard.RecipeVisualizer.render_pie_chart")
@patch("src.visualization.dashboard.RecipeVisualizer.render_score_chart")
@patch("streamlit.write")  # Mocking st.write to capture output when no recipes
def test_render_dashboard(self, mock_write, mock_render_score_chart, mock_render_pie_chart, mock_render_navigation):
    """
    Test the render_dashboard method with different conditions.
    """

    # Mock DataFrame setup (realistic example based on your sample data)
    recipes_data = {
        'name': ['Recipe1', 'Recipe2'],
        'id': [1, 2],
        'nutrition': [[52.0, 0.0, 6.5, 0.0, 1.0, 0.0, 12.0], [387.34, 13.26, 5.0, 0.046, 7.0, 1.6, 60.0]],  # Example nutrition data
        'ingredient_PP': [['squash', 'seasoning'], ['cheese', 'potato']],
        'avg_date': [-1.0, -1.0],  # Example negative date (month)
        'steps': ['["Step1", "Step2"]', '["Step1", "Step2"]'],
        'mtm_score': [50, 60]
    }
    mock_recipes_df = pd.DataFrame(recipes_data)
    mock_interactions_df = pd.DataFrame()  # Mock empty interactions DataFrame

    # Initialize RecipeVisualizer
    visualizer = RecipeVisualizer(mock_recipes_df, mock_interactions_df)

    # Mock current recipe and filtered recipes
    mock_filtered_recipes = mock_recipes_df
    mock_current_recipe = mock_recipes_df.iloc[0]  # First recipe as the current one

    # Mock render_navigation to return the mock data
    mock_render_navigation.return_value = (mock_filtered_recipes, mock_current_recipe)

    # Call render_dashboard
    visualizer.render_dashboard(mock_recipes_df)

    # Assert render_navigation, render_pie_chart, and render_score_chart are called
    mock_render_navigation.assert_called_once_with(mock_recipes_df)
    mock_render_pie_chart.assert_called_once_with(mock_current_recipe)
    mock_render_score_chart.assert_called_once_with(mock_current_recipe)

    # Test with empty DataFrame (no recipes)
    mock_render_navigation.return_value = (pd.DataFrame(), None)  # Empty DataFrame and None current_recipe
    visualizer.render_dashboard(pd.DataFrame())  # Simulate no recipes available

    # Assert that the no recipes message is written to the streamlit interface
    mock_write.assert_called_with("No recipes available.")
    mock_render_navigation.assert_called_once()  # Only called once since no recipes exist

    @patch("streamlit.toggle")
    def test_render_dashboard_ingredients_toggle(self, mock_toggle):
        """
        Test the ingredients toggle functionality in the render_dashboard method.
        """
        selected_recipe = self.recipes_df.iloc[0]
        with patch("streamlit.session_state", {}):
            self.visualizer.render_dashboard(self.recipes_df)

        # Check if toggle button is shown
        mock_toggle.assert_called_once()

        # Simulate toggling ingredients visibility
        show_ingredients = True  # Mocking toggle behavior
        if show_ingredients:
            for ingredient in selected_recipe["ingredient_PP"]:
                # Ensure ingredients are listed
                self.assertIn(ingredient, selected_recipe["ingredient_PP"])


if __name__ == "__main__":
    unittest.main()
    
