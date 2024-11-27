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
    def test_get_sidebar_configurations(
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
        Test the sidebar functionality.
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

        # Mock Streamlit's session_state
        with patch("streamlit.session_state", st_session_state):
            # Mock the multiselect widget
            mock_multiselect.return_value = ["flour", "sugar"]

            # Mock the sliders
            mock_slider.side_effect = [20, 50, 70]  # Mock slider values for protein, carbs, fat

            # Mock the buttons
            mock_button.side_effect = [False, True]  # reset_button, start_search_button

            # Mock expander and columns
            mock_expander.return_value.__enter__.return_value = MagicMock()
            mock_columns.return_value = [MagicMock(), MagicMock()]

            # Call the function
            recipes_df = MagicMock()
            ingredient_list = ["flour", "sugar", "eggs"]
            config = get_sidebar_configurations(recipes_df, ingredient_list)

            # Assertions for returned configuration
            self.assertEqual(config["selected_ingredients"], ["flour", "sugar"])
            self.assertEqual(config["protein_min"], 20)
            self.assertEqual(config["carbs_min"], 50)
            self.assertEqual(config["fat_max"], 70)
            self.assertEqual(config["total_calories"], 770)  # 20*4 + 50*4 + 70*9
            self.assertFalse(config["reset_clicked"])
            self.assertTrue(config["start_search"])

            # Verify widget calls
            mock_multiselect.assert_called_once_with(
                "Type to search ingredients:",
                options=ingredient_list,
                default=[],
                key="selected_ingredients",
                help="Start typing to see suggestions for ingredients.",
            )
            mock_slider.assert_any_call(
                "Minimum Protein (g)", min_value=0, max_value=150, value=20, step=1, key="protein_min"
            )
            mock_slider.assert_any_call(
                "Minimum Carbs (g)", min_value=0, max_value=300, value=50, step=1, key="carbs_min"
            )
            mock_slider.assert_any_call(
                "Maximum Fat (g)", min_value=0, max_value=150, value=70, step=1, key="fat_max"
            )
            mock_button.assert_any_call("Start over", key="reset_button")
            mock_button.assert_any_call("Try My Luck!", key="start_search_button")


if __name__ == "__main__":
    unittest.main()
