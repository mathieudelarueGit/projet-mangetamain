import unittest
from unittest.mock import patch, MagicMock
from src.visualization.front_page import render_front_page


class TestRenderFrontPage(unittest.TestCase):
    """
    Unit tests for the render_front_page function.
    """

    @patch("streamlit.image")
    @patch("streamlit.markdown")
    @patch("streamlit.write")
    @patch("streamlit.header")
    @patch("streamlit.tabs")
    @patch("streamlit.columns")
    @patch("streamlit.link_button")
    def test_render_front_page(
        self,
        mock_link_button,
        mock_columns,
        mock_tabs,
        mock_header,
        mock_write,
        mock_markdown,
        mock_image,
    ):
        """
        Test that the render_front_page function calls the appropriate Streamlit functions.
        """
        # Mock the tabs behavior
        mock_tabs.return_value = [MagicMock(), MagicMock()]

        # Mock the columns
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]

        # Call the function
        render_front_page()

        # Assert that st.image was called with the correct arguments
        mock_image.assert_any_call(
            "src/visualization/images/mangetamain_front_page_banner.jpg",
            use_column_width=True,
        )
        mock_image.assert_any_call(
            "src/visualization/images/fig_ratings_ratios.png", use_column_width=True
        )
        mock_image.assert_any_call(
            "src/visualization/images/fig_dynamics.png", use_column_width=True
        )
        mock_image.assert_any_call(
            "src/visualization/images/ratings.png", use_column_width=True
        )
        mock_image.assert_any_call(
            "src/visualization/images/preparation_time.png", use_column_width=True
        )
        mock_image.assert_any_call(
            "src/visualization/images/word2vec.png", use_column_width=True
        )
        mock_image.assert_any_call(
            "src/visualization/images/top-ingredients.png", use_column_width=True
        )
        mock_image.assert_any_call(
            "src/visualization/images/seasonality.png", use_column_width=True
        )

        # Assert that st.markdown was called with HTML content for the welcome
        # message
        self.assertTrue(mock_markdown.called)
        self.assertIn("Welcome to Mangetamain!", mock_markdown.call_args[0][0])
        self.assertIn(
            '<div style="text-align: justify">', mock_markdown.call_args[0][0]
        )

        # Assert that st.write was called multiple times (for the separator and
        # the seasonal information)
        self.assertTrue(mock_write.called)

        # Assert that st.header was called in the second tab for "Sélection des
        # recettes"
        mock_header.assert_called_with("Sélection des recettes")

        # Check that st.tabs was called with the correct tabs
        mock_tabs.assert_called_once_with(
            ["App purpose", "Data processing behind the scene"]
        )

        # Check that st.columns was called correctly
        mock_columns.assert_called_once()

        # Assert that link button is present with correct arguments
        mock_link_button.assert_called_once_with(
            "Food.com dataset from Kaggle",
            "https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions",
        )


if __name__ == "__main__":
    unittest.main()
