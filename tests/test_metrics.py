import unittest
from metrics import calculate_mtm_score

class TestCalculateMTMScore(unittest.TestCase):
    """
    Unit tests for the calculate_mtm_score function.
    """

    def test_valid_input_high_score(self):
        """
        Test with valid nutrition values that yield a high MTM score.
        """
        nutrition = [400, 20, 10, 3, 15, 5, 50]  # [calories, fat, sugar, sodium, protein, saturated_fat, carbs]
        score = calculate_mtm_score(nutrition)
        self.assertEqual(score, 100)  # Expect maximum score

    def test_valid_input_low_score(self):
        """
        Test with valid nutrition values that yield a low MTM score.
        """
        nutrition = [2000, 50, 50, 10, 5, 20, 20]  # [calories, fat, sugar, sodium, protein, saturated_fat, carbs]
        score = calculate_mtm_score(nutrition)
        self.assertEqual(score, 0)  # Expect minimum score

    def test_invalid_input_type(self):
        """
        Test with invalid nutrition type (not a list or tuple).
        """
        nutrition = "invalid_data"  # Invalid type
        score = calculate_mtm_score(nutrition)
        self.assertEqual(score, 0)  # Expect default 0 for invalid input

    def test_invalid_input_length(self):
        """
        Test with a nutrition list that has fewer than 7 elements.
        """
        nutrition = [400, 20, 10]  # Too short
        score = calculate_mtm_score(nutrition)
        self.assertEqual(score, 0)  # Expect default 0 for invalid input

    def test_edge_case_calories_in_range(self):
        """
        Test with edge case where calories are exactly at the threshold.
        """
        nutrition = [200, 20, 10, 3, 15, 5, 50]  # Lower threshold for calories
        score = calculate_mtm_score(nutrition)
        self.assertGreater(score, 0)  # Expect a positive score

    def test_edge_case_high_calories(self):
        """
        Test with edge case where calories are slightly above the upper threshold.
        """
        nutrition = [1501, 20, 10, 3, 15, 5, 50]  # Above the upper threshold
        score = calculate_mtm_score(nutrition)
        self.assertGreater(score, 0)  # Still expect a positive score, but with a penalty

    def test_balanced_nutrition_bonus(self):
        """
        Test with balanced fat and protein values to check for bonus points.
        """
        nutrition = [400, 20, 10, 3, 15, 5, 50]  # Balanced fat and protein
        score = calculate_mtm_score(nutrition)
        self.assertGreaterEqual(score, 70)  # Expect a boosted score due to balance bonus

    def test_negative_factors(self):
        """
        Test with high values for negative factors to check for penalties.
        """
        nutrition = [400, 40, 50, 6, 5, 20, 30]  # High fat, sugar, sodium, and saturated fat
        score = calculate_mtm_score(nutrition)
        self.assertLess(score, 50)  # Expect penalties to lower the score

    def test_maximum_constraints(self):
        """
        Test that the score does not exceed 100.
        """
        nutrition = [400, 15, 10, 3, 20, 5, 60]  # High-quality recipe
        score = calculate_mtm_score(nutrition)
        self.assertEqual(score, 100)  # Score should be capped at 100

    def test_minimum_constraints(self):
        """
        Test that the score does not drop below 0.
        """
        nutrition = [2000, 50, 50, 10, 5, 20, 20]  # Poor-quality recipe
        score = calculate_mtm_score(nutrition)
        self.assertEqual(score, 0)  # Score should be floored at 0

if __name__ == "__main__":
    unittest.main()
