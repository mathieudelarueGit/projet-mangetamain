import unittest
import pandas as pd
from filter import RecipeFilter

class TestRecipeFilter(unittest.TestCase):
    """
    Unit tests for the RecipeFilter class.
    """

    def setUp(self):
        """
        Set up a sample DataFrame for testing.
        """
        self.sample_data = pd.DataFrame({
            "ingredients": [
                ["flour", "sugar", "butter"],
                ["flour", "milk", "eggs"],
                ["chicken", "rice", "peas"],
                ["fish", "lemon", "garlic"],
            ],
            "nutrition": [
                [200, 10, 15, 30, 20, 5, 50],  # Example: [calories, fat, protein, fiber, etc.]
                [150, 5, 10, 20, 25, 3, 40],
                [300, 15, 20, 35, 10, 7, 30],
                [250, 12, 18, 25, 15, 6, 35],
            ],
        })
        self.recipe_filter = RecipeFilter(self.sample_data)

    def test_filter_by_ingredients(self):
        """
        Test filtering recipes by selected ingredients.
        """
        selected_ingredients = ["flour", "sugar", "butter"]
        self.recipe_filter.filter_by_ingredients(selected_ingredients)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 1)
        self.assertEqual(filtered_recipes.iloc[0]["ingredients"], ["flour", "sugar", "butter"])

    def test_filter_by_nutrition_protein(self):
        """
        Test filtering recipes by minimum protein value.
        """
        self.recipe_filter.filter_by_nutrition(protein_min=18)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 2)
        self.assertTrue(all(recipe[2] >= 18 for recipe in filtered_recipes["nutrition"]))

    def test_filter_by_nutrition_carbs(self):
        """
        Test filtering recipes by minimum carbohydrates value.
        """
        self.recipe_filter.filter_by_nutrition(carbs_min=40)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 2)
        self.assertTrue(all(recipe[6] >= 40 for recipe in filtered_recipes["nutrition"]))

    def test_filter_by_nutrition_fat(self):
        """
        Test filtering recipes by maximum fat value.
        """
        self.recipe_filter.filter_by_nutrition(fat_max=10)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 1)
        self.assertTrue(all(recipe[1] <= 10 for recipe in filtered_recipes["nutrition"]))

    def test_combined_filters(self):
        """
        Test combining ingredient and nutritional filters.
        """
        selected_ingredients = ["flour", "milk", "eggs"]
        self.recipe_filter.filter_by_ingredients(selected_ingredients)
        self.recipe_filter.filter_by_nutrition(protein_min=18)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 0)  # No recipes match both criteria

    def test_empty_filtered_recipes(self):
        """
        Test behavior when no recipes match filters.
        """
        self.recipe_filter.filter_by_ingredients(["nonexistent"])
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertTrue(filtered_recipes.empty)

    def test_reset_filtered_recipes(self):
        """
        Test that filtering starts with the original dataset each time.
        """
        # First filter
        self.recipe_filter.filter_by_ingredients(["flour", "sugar", "butter"])
        filtered_recipes_first = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes_first), 1)

        # Reset filter
        self.recipe_filter.filtered_recipes = self.recipe_filter.recipes_df.copy()

        # Second filter
        self.recipe_filter.filter_by_ingredients(["chicken", "rice", "peas"])
        filtered_recipes_second = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes_second), 1)
        self.assertEqual(filtered_recipes_second.iloc[0]["ingredients"], ["chicken", "rice", "peas"])

if __name__ == "__main__":
    unittest.main()
