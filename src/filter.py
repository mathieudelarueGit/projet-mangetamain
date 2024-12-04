import logging
import pandas as pd

# Create a logger for the RecipeFilter class
logger = logging.getLogger(__name__)


class RecipeFilter:
    """
    A class to filter recipes based on ingredients and nutritional values.
    """

    def __init__(self, recipes_df: pd.DataFrame) -> None:
        """
        Initialize the RecipeFilter with the original DataFrame.

        Parameters:
        ----------
        recipes_df : pd.DataFrame
            DataFrame containing the recipes data.
        """
        self.recipes_df = recipes_df.copy()
        self.filtered_recipes = recipes_df.copy()
        logger.info("RecipeFilter initialized with %d recipes.", len(recipes_df))

    def check_empty(self) -> bool:
        """
        Check if the filtered DataFrame is empty.

        Returns:
        -------
        bool
            True if the DataFrame is empty, otherwise False.
        """
        if self.filtered_recipes.empty:
            logger.warning("No rows left after filtering!")
            return True
        return False

    def filter_by_ingredients(self, selected_ingredients: list) -> None:
        """
        Filter recipes based on the selected ingredients.

        Parameters:
        ----------
        selected_ingredients : list
            List of ingredients to filter recipes by. A recipe is returned
            only if all its ingredients are in the selected list.
        """
        if self.filtered_recipes.empty:
            logger.info("Skipping ingredient filtering; no recipes available.")
            return

        if not selected_ingredients:
            logger.info("No ingredients selected; keeping all recipes.")
            return  # Keep all recipes if no ingredients are selected

        if "ingredient_PP" in self.recipes_df.columns:

            def recipe_matches(recipe_ingredients: list) -> bool:
                """
                Check if all recipe ingredients are in the selected ingredients.

                Parameters:
                ----------
                recipe_ingredients : list
                    List of ingredients in the recipe.

                Returns:
                -------
                bool
                    True if all recipe ingredients are in the selected ingredients.
                """
                return set(recipe_ingredients).issubset(set(selected_ingredients))

            self.filtered_recipes = self.filtered_recipes[
                self.filtered_recipes["ingredient_PP"].apply(recipe_matches)
            ]
            logger.info(
                "Filtered by ingredients; %d recipes remain.",
                len(self.filtered_recipes),
            )
        else:
            self.filtered_recipes = self.filtered_recipes.iloc[0:0]  # Empty DataFrame
            logger.warning("No 'ingredient_PP' column found; reset to empty DataFrame.")

    def filter_by_nutrition(
        self, protein_min: int = 0, carbs_min: int = 0, fat_max: int = 150
    ) -> None:
        """
        Filter recipes by nutritional values.

        Parameters:
        ----------
        protein_min : int, optional
            Minimum protein value (default is 0).
        carbs_min : int, optional
            Minimum carbs value (default is 0).
        fat_max : int, optional
            Maximum fat value (default is 150).
        """
        if self.filtered_recipes.empty:
            logger.info("Skipping nutrition filtering; no recipes available.")
            return

        if "nutrition" in self.recipes_df.columns:
            # Filter by protein
            if protein_min > 0:
                self.filtered_recipes = self.filtered_recipes[
                    self.filtered_recipes["nutrition"].apply(
                        lambda x: (
                            isinstance(x, (list, tuple))
                            and len(x) > 4
                            and x[4] >= protein_min
                        )
                    )
                ]
                logger.info(
                    "Filtered by protein (min %d); %d recipes remain.",
                    protein_min,
                    len(self.filtered_recipes),
                )
                if self.check_empty():
                    return

            # Filter by carbs
            if carbs_min > 0:
                self.filtered_recipes = self.filtered_recipes[
                    self.filtered_recipes["nutrition"].apply(
                        lambda x: (
                            isinstance(x, (list, tuple))
                            and len(x) > 6
                            and x[6] >= carbs_min
                        )
                    )
                ]
                logger.info(
                    "Filtered by carbs (min %d); %d recipes remain.",
                    carbs_min,
                    len(self.filtered_recipes),
                )
                if self.check_empty():
                    return

            # Filter by fat
            if fat_max < 150:
                self.filtered_recipes = self.filtered_recipes[
                    self.filtered_recipes["nutrition"].apply(
                        lambda x: (
                            isinstance(x, (list, tuple))
                            and len(x) > 1
                            and x[1] <= fat_max
                        )
                    )
                ]
                logger.info(
                    "Filtered by fat (max %d); %d recipes remain.",
                    fat_max,
                    len(self.filtered_recipes),
                )
                if self.check_empty():
                    return
        else:
            logger.warning("No 'nutrition' column found; skipping nutrition filtering.")

    def get_filtered_recipes(self) -> pd.DataFrame:
        """
        Get the filtered DataFrame.

        Returns:
        -------
        pd.DataFrame
            The DataFrame containing the filtered recipes.
        """
        logger.info("Returning %d filtered recipes.", len(self.filtered_recipes))
        return self.filtered_recipes
