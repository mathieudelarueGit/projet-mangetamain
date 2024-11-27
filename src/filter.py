import pandas as pd


class RecipeFilter:
    def __init__(self, recipes_df: pd.DataFrame):
        """
        Initialize the RecipeFilter with the original DataFrame.
        """
        self.recipes_df = recipes_df.copy()
        self.filtered_recipes = recipes_df.copy()

    def check_empty(self):
        """
        Check if the filtered DataFrame is empty. If it is, stop further filtering.
        """
        if self.filtered_recipes.empty:
            print("No rows left after filtering!")
            return True
        return False

    def filter_by_ingredients(self, selected_ingredients):
        """
        Filter recipes based on selected ingredients.
        A recipe is returned only if all its ingredients are present
        in the selected ingredients.
        """

        if self.filtered_recipes.empty:
            return

        if not selected_ingredients:  # If no ingredients are selected
            return  # Do nothing and keep all recipes

        if "ingredients" in self.recipes_df.columns and selected_ingredients:

            def recipe_matches(recipe_ingredients):
                """
                Check if all ingredients in the recipe are in the selected ingredients.
                """
                is_subset = set(recipe_ingredients).issubset(set(selected_ingredients))
                return is_subset

            # Filter recipes
            self.filtered_recipes = self.filtered_recipes[
                self.filtered_recipes["ingredients"].apply(recipe_matches)
            ]
        else:
            # If no selected ingredients, reset to empty DataFrame
            self.filtered_recipes = self.filtered_recipes.iloc[0:0]  # Empty DataFrame

    def filter_by_nutrition(self, protein_min=0, carbs_min=0, fat_max=150):
        """
        Filter recipes by nutritional values.
        """
        if self.filtered_recipes.empty:
            return

        if "nutrition" in self.recipes_df.columns:
            # Filter by protein
            if protein_min > 0:
                self.filtered_recipes = self.filtered_recipes[
                    self.filtered_recipes["nutrition"].apply(
                        lambda x: (
                            isinstance(x, (list, tuple)) and
                            len(x) > 4 and
                            x[4] >= protein_min
                        )
                    )
                ]

                if self.check_empty():
                    return

            # Filter by carbs
            if carbs_min > 0:
                self.filtered_recipes = self.filtered_recipes[
                    self.filtered_recipes["nutrition"].apply(
                        lambda x: (
                            isinstance(x, (list, tuple)) and
                            len(x) > 6 and
                            x[6] >= carbs_min
                        )
                    )
                ]

                if self.check_empty():
                    return

            # Filter by fat
            if fat_max < 150:
                self.filtered_recipes = self.filtered_recipes[
                    self.filtered_recipes["nutrition"].apply(
                        lambda x: (
                            isinstance(x, (list, tuple)) and
                            len(x) > 1 and
                            x[1] <= fat_max
                        )
                    )
                ]

                if self.check_empty():
                    return

    def get_filtered_recipes(self):
        """
        Return the filtered DataFrame.
        """
        return self.filtered_recipes
