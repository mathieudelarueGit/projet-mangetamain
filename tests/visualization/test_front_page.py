import unittest
from unittest.mock import patch
import front_page


class TestRenderFrontPage(unittest.TestCase):
    """
    Unit tests for the render_front_page function.
    """

    @patch("streamlit.image")
    @patch("streamlit.markdown")
    def test_render_front_page(self, mock_markdown, mock_image):
        """
        Test that the render_front_page function calls the appropriate Streamlit functions.
        """
        # Call the function
        front_page.render_front_page()

        # Assert that st.image was called with the correct arguments
        mock_image.assert_called_once_with(
            "src/visualization/images/mangetamain_front_page_banner.jpg",
            use_column_width=True,
        )

        # Assert that st.markdown was called once
        self.assertTrue(mock_markdown.called)
        # Optionally, check the first few words of the HTML content
        self.assertIn("Welcome to Mangetamain!", mock_markdown.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
