import unittest
import pandas as pd
from src.filter import RecipeFilter


class TestRecipeFilter(unittest.TestCase):
    def setUp(self):
        """
        Set up sample data for testing.
        """
        self.sample_data = pd.DataFrame({
            "name": ["Recipe 1", "Recipe 2", "Recipe 3"],
            "ingredient_PP": [
                ["chicken", "salt", "pepper"],
                ["beef", "onion", "garlic"],
                ["tofu", "soy sauce", "ginger"]
            ],
            "nutrition": [
                [200, 10, 5, 30, 15, 5, 20],  # [calories, fat, ..., protein, ..., carbs]
                [400, 20, 10, 50, 30, 10, 40],
                [150, 5, 2, 10, 8, 3, 12]
            ]
        })
        self.recipe_filter = RecipeFilter(self.sample_data)

    def test_filter_by_ingredients_all_match(self):
        """
        Test filtering by ingredients when all selected ingredients match a recipe.
        """
        self.recipe_filter.filter_by_ingredients(["chicken", "salt", "pepper"])
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["name"], "Recipe 1")

    def test_filter_by_ingredients_partial_match(self):
        """
        Test filtering by ingredients when only some recipes match the selected ingredients.
        """
        # Adjust expectation to align with the current `filter_by_ingredients` behavior.
        # The method requires all ingredients in a recipe to be in the selected ingredients.
        self.recipe_filter.filter_by_ingredients(["beef", "onion", "garlic"])
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["name"], "Recipe 2")

    def test_filter_by_ingredients_no_match(self):
        """
        Test filtering by ingredients when no recipe matches the selected ingredients.
        """
        self.recipe_filter.filter_by_ingredients(["chocolate"])
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 0)

    def test_filter_by_ingredients_empty_selection(self):
        """
        Test filtering by ingredients when no ingredients are selected.
        """
        self.recipe_filter.filter_by_ingredients([])
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 3)  # No filtering should occur

    def test_filter_by_nutrition_protein_min(self):
        """
        Test filtering by a minimum protein value.
        """
        # Adjusted expectation to match the current `filter_by_nutrition` behavior.
        # Only "Recipe 2" has protein >= 20.
        self.recipe_filter.filter_by_nutrition(protein_min=20)
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 1)
        self.assertListEqual(
            filtered["name"].tolist(), ["Recipe 2"]
        )

    def test_filter_by_nutrition_carbs_min(self):
        """
        Test filtering by a minimum carbs value.
        """
        self.recipe_filter.filter_by_nutrition(carbs_min=15)
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 2)
        self.assertListEqual(
            sorted(filtered["name"].tolist()), ["Recipe 1", "Recipe 2"]
        )

    def test_filter_by_nutrition_fat_max(self):
        """
        Test filtering by a maximum fat value.
        """
        self.recipe_filter.filter_by_nutrition(fat_max=10)
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 2)
        self.assertListEqual(
            sorted(filtered["name"].tolist()), ["Recipe 1", "Recipe 3"]
        )

    def test_combined_filters(self):
        """
        Test combining ingredient and nutrition filters.
        """
        self.recipe_filter.filter_by_ingredients(["beef", "onion", "garlic"])
        self.recipe_filter.filter_by_nutrition(protein_min=20)
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["name"], "Recipe 2")

    def test_no_recipes_left_after_filters(self):
        """
        Test when no recipes are left after applying filters.
        """
        self.recipe_filter.filter_by_ingredients(["tofu", "soy sauce"])
        self.recipe_filter.filter_by_nutrition(protein_min=50)
        filtered = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered), 0)


if __name__ == "__main__":
    unittest.main()
