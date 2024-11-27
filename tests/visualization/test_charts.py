import unittest
import pandas as pd
from plotly.graph_objects import Figure
from src.visualization.charts import ChartFactory


class TestChartFactory(unittest.TestCase):
    """
    Unit tests for the ChartFactory class.
    """

    def setUp(self):
        """
        Set up sample data for testing.
        """
        self.sample_labels = ["Protein", "Fat", "Carbs"]
        self.sample_values = [40, 30, 30]
        self.sample_title = "Test Nutritional Breakdown"

        self.sample_data = pd.DataFrame({
            "Date": ["2023-01-01", "2023-02-01", "2023-03-01"],
            "Interactions": [100, 150, 200],
            "Recipe": ["Recipe A", "Recipe B", "Recipe C"],
            "Proportion (%)": [50, 30, 20],
            "Color": ["Red", "Green", "Blue"],
            "Text": ["50%", "30%", "20%"],
        })

        self.mtm_score = 75
        self.nutrition = [400, 20, 10, 3, 15, 5, 50]

    def test_pie_chart(self):
        """
        Test the pie_chart method.
        """
        chart = ChartFactory.pie_chart(
            labels=self.sample_labels, values=self.sample_values, title=self.sample_title
        )
        self.assertIsInstance(chart, Figure)
        self.assertEqual(chart.layout.title.text, self.sample_title)
        self.assertEqual(len(chart.data), 1)
        self.assertEqual(chart.data[0].type, "pie")

    def test_bar_chart(self):
        """
        Test the bar_chart method.
        """
        chart = ChartFactory.bar_chart(
            data=self.sample_data,
            x_col="Recipe",
            y_col="Proportion (%)",
            color_col="Color",
            text_col="Text",
            title="Test Bar Chart",
        )
        self.assertIsInstance(chart, Figure)
        self.assertEqual(chart.layout.title.text, "Test Bar Chart")
        self.assertEqual(len(chart.data), 3)  # Three bars for three recipes
        self.assertEqual(chart.data[0].type, "bar")

    def test_popularity_chart(self):
        """
        Test the popularity_chart method.
        """
        chart = ChartFactory.popularity_chart(
            data=self.sample_data, x_col="Date", y_col="Interactions", title="Test Popularity Chart"
        )
        self.assertIsInstance(chart, Figure)
        self.assertEqual(chart.layout.title.text, "Test Popularity Chart")
        self.assertEqual(len(chart.data), 1)
        self.assertEqual(chart.data[0].type, "scatter")
        self.assertEqual(chart.data[0].mode, "lines")

    def test_score_display(self):
        """
        Test the score_display method.
        """
        chart = ChartFactory.score_display(
            mtm_score=self.mtm_score, nutrition=self.nutrition
        )
        self.assertIsInstance(chart, Figure)
        self.assertIn("Healthiness Score", chart.layout.annotations[0].text)
        self.assertIn(str(self.mtm_score), chart.layout.annotations[0].text)
        self.assertEqual(chart.layout.height, 400)
        self.assertEqual(chart.layout.width, 400)

    def test_score_display_low_score(self):
        """
        Test the score_display method with a low score.
        """
        chart = ChartFactory.score_display(mtm_score=25, nutrition=self.nutrition)
        self.assertIn("red", chart.layout.annotations[0].text)

    def test_score_display_high_score(self):
        """
        Test the score_display method with a high score.
        """
        chart = ChartFactory.score_display(mtm_score=90, nutrition=self.nutrition)
        self.assertIn("green", chart.layout.annotations[0].text)


if __name__ == "__main__":
    unittest.main()
