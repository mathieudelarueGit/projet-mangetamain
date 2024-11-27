import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from dashboard import RecipeVisualizer


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
            "nutrition": [
                [400, 20, 10, 3, 15, 5, 50],
                [300, 15, 8, 2, 10, 4, 30],
                [500, 25, 12, 4, 20, 6, 70],
            ],
            "mtm_score": [75, 60, 85],
        })

        self.interactions_df = pd.DataFrame({
            "recipe_id": [1, 1, 2, 3, 3, 3],
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06"],
        })

        self.visualizer = RecipeVisualizer(self.recipes_df, self.interactions_df)

    @patch("streamlit.columns")
    @patch("streamlit.session_state", {})
    def test_render_navigation(self, mock_columns):
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
        self.assertTrue(mock_plotly_chart.called)

    @patch("streamlit.plotly_chart")
    def test_render_popularity_chart(self, mock_plotly_chart):
        """
        Test the render_popularity_chart method.
        """
        selected_recipe = self.recipes_df.iloc[0]
        self.visualizer.render_popularity_chart(selected_recipe)

        # Assert that plotly_chart was called once
        self.assertTrue(mock_plotly_chart.called)

    @patch("streamlit.plotly_chart")
    def test_render_score_chart(self, mock_plotly_chart):
        """
        Test the render_score_chart method.
        """
        selected_recipe = self.recipes_df.iloc[0]
        self.visualizer.render_score_chart(selected_recipe)

        # Assert that plotly_chart was called once
        self.assertTrue(mock_plotly_chart.called)

    @patch("dashboard.RecipeVisualizer.render_navigation")
    @patch("dashboard.RecipeVisualizer.render_pie_chart")
    @patch("dashboard.RecipeVisualizer.render_score_chart")
    def test_render_dashboard(self, mock_render_navigation, mock_render_pie_chart, mock_render_score_chart):
        """
        Test the render_dashboard method.
        """
        mock_render_navigation.return_value = self.recipes_df.iloc[0]
        self.visualizer.render_dashboard(self.recipes_df)

        # Assert that all rendering methods are called
        self.assertTrue(mock_render_navigation.called)
        self.assertTrue(mock_render_pie_chart.called)
        self.assertTrue(mock_render_score_chart.called)


if __name__ == "__main__":
    unittest.main()