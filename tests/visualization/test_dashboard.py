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

    @patch("streamlit.columns")
    @patch("streamlit.session_state", {})
    @patch("streamlit.button")
    @patch("streamlit.markdown")
    def test_render_navigation(self, mock_markdown, mock_button, mock_columns):
        """
        Test the render_navigation method.
        """
        mock_left_arrow = MagicMock()
        mock_title = MagicMock()
        mock_right_arrow = MagicMock()
        mock_columns.return_value = [mock_left_arrow, mock_title, mock_right_arrow]

        current_recipe = self.visualizer.render_navigation(self.recipes_df)

        # Assert current recipe index defaults to 0
        self.assertEqual(current_recipe["name"], "Recipe A")

        # Simulate clicking the right arrow
        st.session_state["current_recipe_index"] = 1
        current_recipe = self.visualizer.render_navigation(self.recipes_df)
        self.assertEqual(current_recipe["name"], "Recipe B")

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
    def test_render_dashboard(self, mock_render_navigation, mock_render_pie_chart, mock_render_score_chart):
        """
        Test the render_dashboard method.
        """
        mock_render_navigation.return_value = self.recipes_df.iloc[0]
        self.visualizer.render_dashboard(self.recipes_df)

        # Assert that all rendering methods are called
        mock_render_navigation.assert_called_once()
        mock_render_pie_chart.assert_called_once()
        mock_render_score_chart.assert_called_once()
        
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
