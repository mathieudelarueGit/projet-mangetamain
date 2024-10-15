import unittest
from src.models.algorithm import Algorithm

class TestAlgorithm(unittest.TestCase):
    
    def setUp(self):
        """Set up a default Algorithm instance for testing."""
        self.algo = Algorithm(name="TestAlgorithm")

    def test_initialization(self):
        """Test if the algorithm is initialized with the correct name and empty parameters."""
        self.assertEqual(self.algo.name, "TestAlgorithm")
        self.assertEqual(self.algo.params, {})

    def test_set_param(self):
        """Test if parameters can be set and updated."""
        self.algo.set_param('learning_rate', 0.01)
        self.assertEqual(self.algo.get_param('learning_rate'), 0.01)

        # Update the parameter and check again
        self.algo.set_param('learning_rate', 0.05)
        self.assertEqual(self.algo.get_param('learning_rate'), 0.05)

    def test_get_param(self):
        """Test if getting a non-existent parameter returns None."""
        self.assertIsNone(self.algo.get_param('non_existent_param'))

    def test_model_info(self):
        """Test if the model_info method returns the correct summary."""
        self.algo.set_param('max_depth', 10)
        info = self.algo.model_info()
        self.assertEqual(info['name'], 'TestAlgorithm')
        self.assertEqual(info['params']['max_depth'], 10)