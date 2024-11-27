import unittest
import pandas as pd
from src.filter import RecipeFilter


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
                [200, 10, 15, 30, 20, 5, 50],  # [calories, fat, protein, fiber, etc.]
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
        selected_ingredients = ["flour", "milk", "eggs"]
        self.recipe_filter.filter_by_ingredients(selected_ingredients)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 1)
        self.assertEqual(
            filtered_recipes.iloc[0]["ingredients"], ["flour", "milk", "eggs"]
        )

    def test_filter_by_ingredients_empty(self):
        """
        Test filtering with ingredients that don't exist in any recipe.
        """
        self.recipe_filter.filter_by_ingredients(["nonexistent"])
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertTrue(filtered_recipes.empty)

    def test_filter_by_ingredients_no_selection(self):
        """
        Test filtering with an empty selection of ingredients.
        """
        self.recipe_filter.filter_by_ingredients([])
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), len(self.sample_data))

    def test_filter_by_nutrition_protein(self):
        """
        Test filtering recipes by minimum protein value.
        """
        self.recipe_filter.filter_by_nutrition(protein_min=18)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 2)

    def test_filter_by_nutrition_fat(self):
        """
        Test filtering recipes by maximum fat value.
        """
        self.recipe_filter.filter_by_nutrition(fat_max=10)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 2)

    def test_filter_by_nutrition_carbs(self):
        """
        Test filtering recipes by minimum carbs value.
        """
        self.recipe_filter.filter_by_nutrition(carbs_min=40)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 2)

    def test_combined_filters(self):
        """
        Test combining ingredient and nutritional filters.
        """
        selected_ingredients = ["flour", "milk", "eggs"]
        self.recipe_filter.filter_by_ingredients(selected_ingredients)
        self.recipe_filter.filter_by_nutrition(protein_min=10)
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertEqual(len(filtered_recipes), 1)
        self.assertEqual(
            filtered_recipes.iloc[0]["ingredients"], ["flour", "milk", "eggs"]
        )

    def test_no_matching_combined_filters(self):
        """
        Test combining filters where no recipes match.
        """
        selected_ingredients = ["flour", "milk", "eggs"]
        self.recipe_filter.filter_by_ingredients(selected_ingredients)
        self.recipe_filter.filter_by_nutrition(protein_min=50)  # No recipes have protein >= 50
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertTrue(filtered_recipes.empty)

    def test_empty_filtered_recipes(self):
        """
        Test behavior when no recipes match filters.
        """
        self.recipe_filter.filter_by_ingredients(["nonexistent"])
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        self.assertTrue(filtered_recipes.empty)

    def test_get_filtered_recipes_initial(self):
        """
        Test the get_filtered_recipes method before any filtering.
        """
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        pd.testing.assert_frame_equal(filtered_recipes, self.sample_data)

    def test_reset_filtered_recipes(self):
        """
        Test resetting the filtered recipes to the original data.
        """
        self.recipe_filter.filter_by_ingredients(["flour", "milk", "eggs"])
        self.recipe_filter.filtered_recipes = self.recipe_filter.recipes_df.copy()
        filtered_recipes = self.recipe_filter.get_filtered_recipes()
        pd.testing.assert_frame_equal(filtered_recipes, self.sample_data)


if __name__ == "__main__":
    unittest.main()
