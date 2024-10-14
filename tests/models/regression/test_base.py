import unittest
import numpy as np
from src.models.regression.base import BaseRegression

# Mock class for testing BaseRegression (since it's abstract)
class MockRegression(BaseRegression):
    def fit(self):
        pass

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.ones(X.shape[0])  # Mock predict method returning ones

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.mean(y_true - y_pred)  # Mock evaluate method (Mean error)


class TestBaseRegression(unittest.TestCase):

    def setUp(self):
        """Set up test data and MockRegression instance."""
        self.X = np.array([[1, 2], [3, 4], [5, 6]])
        self.y = np.array([1, 2, 3])
        self.model = MockRegression(name="MockRegression", X=self.X, y=self.y)

    def test_initialization(self):
        """Test initialization of BaseRegression."""
        self.assertEqual(self.model.name, "MockRegression")
        np.testing.assert_array_equal(self.model.X, self.X)
        np.testing.assert_array_equal(self.model.y, self.y)

    def test_predict(self):
        """Test the predict method of BaseRegression."""
        predictions = self.model.predict(self.X)
        expected_predictions = np.ones(self.X.shape[0])  # Expecting ones as per mock implementation
        np.testing.assert_array_equal(predictions, expected_predictions)

    def test_evaluate(self):
        """Test the evaluate method of BaseRegression."""
        predictions = self.model.predict(self.X)
        result = self.model.evaluate(self.y, predictions)
        expected_result = np.mean(self.y - predictions)  # Mean error
        self.assertAlmostEqual(result, expected_result, places=5)