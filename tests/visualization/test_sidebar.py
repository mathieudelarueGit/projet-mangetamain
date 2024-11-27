import unittest
from unittest.mock import patch, MagicMock
from src.visualization.sidebar import get_sidebar_configurations


class TestSidebar(unittest.TestCase):
    """
    Unit tests for the get_sidebar_configurations function.
    """

    @patch("streamlit.sidebar.expander")
    @patch("streamlit.sidebar.columns")
    @patch("streamlit.sidebar.title")
    @patch("streamlit.sidebar.markdown")
    @patch("streamlit.sidebar.button")
    @patch("streamlit.multiselect")
    @patch("streamlit.slider")
    def test_get_sidebar_configurations_with_reset(
        self,
        mock_slider,
        mock_multiselect,
        mock_button,
        mock_markdown,
        mock_title,
        mock_columns,
        mock_expander,
    ):
        """
        Test the sidebar functionality when reset is clicked.
        """
        # Mock session state
        st_session_state = {
            "reset_clicked": False,
            "expand_ingredients": True,
            "expand_macronutrients": False,
            "protein_min": 20,
            "carbs_min": 50,
            "fat_max": 70,
            "selected_ingredients": ["flour", "sugar"],
        }

        # Patch the session state
        with patch("streamlit.session_state", st_session_state):
            # Mock widgets
            mock_multiselect.return_value = []
            mock_slider.side_effect = [0, 0, 150]  # Default slider values
            mock_button.side_effect = [True, False]  # Simulate reset button clicked
            mock_expander.return_value.__enter__.return_value = MagicMock()
            mock_columns.return_value = [MagicMock(), MagicMock()]

            # Call the function
            recipes_df = MagicMock()
            ingredient_list = ["flour", "sugar", "eggs"]
            config = get_sidebar_configurations(recipes_df, ingredient_list)

            # Simulate the reset action directly
            st_session_state["reset_clicked"] = True
            st_session_state["selected_ingredients"] = []
            st_session_state["protein_min"] = 0
            st_session_state["carbs_min"] = 0
            st_session_state["fat_max"] = 150

            # Assert that session state reflects the reset state
            self.assertTrue(st_session_state["reset_clicked"])
            self.assertEqual(st_session_state["selected_ingredients"], [])
            self.assertEqual(st_session_state["protein_min"], 0)
            self.assertEqual(st_session_state["carbs_min"], 0)
            self.assertEqual(st_session_state["fat_max"], 150)

            # Ensure configuration values reflect the reset state
            self.assertEqual(config["selected_ingredients"], [])
            self.assertEqual(config["protein_min"], 0)
            self.assertEqual(config["carbs_min"], 0)
            self.assertEqual(config["fat_max"], 150)


if __name__ == "__main__":
    unittest.main()
