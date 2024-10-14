import unittest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from src.models.regression.linear_regression import LinearRegressionModel

class TestLinearRegressionModel(unittest.TestCase):

    def setUp(self):
        """Set up test data and LinearRegressionModel instance."""
        self.X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
        self.y = np.array([3, 5, 7, 9])
        self.model = LinearRegressionModel(X=self.X, y=self.y)

    def test_initialization(self):
        """Test the initialization of LinearRegressionModel."""
        self.assertEqual(self.model.name, 'LinearRegression')
        np.testing.assert_array_equal(self.model.X, self.X)
        np.testing.assert_array_equal(self.model.y, self.y)
        self.assertIsInstance(self.model.model, LinearRegression)

    def test_fit(self):
        """Test the fit method of LinearRegressionModel."""
        self.model.fit()
        self.assertTrue(hasattr(self.model.model, 'coef_'))  # Model should have learned coefficients

    def test_predict(self):
        """Test the predict method of LinearRegressionModel."""
        self.model.fit()
        predictions = self.model.predict(self.X)
        expected_predictions = np.array([3, 5, 7, 9])  # Since we created a perfect linear relation
        np.testing.assert_almost_equal(predictions, expected_predictions, decimal=5)

    def test_evaluate(self):
        """Test the evaluate method of LinearRegressionModel using R-squared."""
        self.model.fit()
        predictions = self.model.predict(self.X)
        r_squared = self.model.evaluate(self.y, predictions)
        expected_r_squared = r2_score(self.y, predictions)
        self.assertAlmostEqual(r_squared, expected_r_squared, places=5)