import logging
import streamlit as st
import pandas as pd

from src.visualization.sidebar import get_sidebar_configurations
from src.visualization.dashboard import RecipeVisualizer
from src.visualization.front_page import render_front_page
from src.data_loader import DataLoader
from src.filter import RecipeFilter
from src.log_config import setup_logging


class RecipeApp:
    """
    Main application class for running the recipe filtering and visualization.
    """

    def __init__(self) -> None:
        """
        Initialize the application by setting up logging and loading data.
        """
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing RecipeApp...")

        # Load data
        self.data_loader = DataLoader()
        self.logger.info("Loading recipes and interactions data...")
        self.recipes_df, self.ingredient_list = self.data_loader.load_and_parse_data(
            "dataset/PP_recipes_final.csv.zip"
        )
        self.interactions_df = self.data_loader.load_data(
            "dataset/PP_interactions_final.csv.zip"
        )
        self.interactions_df["date"] = pd.to_datetime(self.interactions_df["date"])
        self.filtered_recipes = None

    def run(self) -> None:
        """
        Main function to run the app logic, including sidebar interactions
        and recipe filtering.
        """
        self.logger.info("Running RecipeApp...")
        user_inputs = get_sidebar_configurations(self.recipes_df, self.ingredient_list)

        # Check if any recipe button is clicked
        self.check_recipe_buttons_in_main(user_inputs)

        # Handle reset action
        if user_inputs["reset_clicked"]:
            self.logger.info("Reset button clicked.")
            self.reset_session_state()

        # Handle search action
        if user_inputs["start_search"]:
            if user_inputs["recipe_clicked"]:
                self.filtered_recipes = st.session_state["filtered_recipes"]
            else:
                self.logger.info("Filtering recipes based on user inputs.")
                self.filtered_recipes = self.filter_recipes(user_inputs)
            self.display_results(user_inputs)
        else:
            self.filtered_recipes = st.session_state.get("filtered_recipes", None)
            self.display_dashboard_or_message()

    def reset_session_state(self) -> None:
        """
        Reset the app state and rerun the Streamlit app.
        """
        self.logger.info("Resetting session state.")
        render_front_page()
        st.session_state.clear()
        st.rerun()

    def filter_recipes(self, user_inputs: dict) -> pd.DataFrame:
        """
        Apply ingredient and nutritional filters to the recipes.

        Parameters:
        ----------
        user_inputs : dict
            Dictionary containing user-selected filters.

        Returns:
        -------
        pd.DataFrame
            Filtered recipes based on user inputs.
        """
        self.logger.debug("Applying filters: %s", user_inputs)
        recipe_filter = RecipeFilter(self.recipes_df)
        recipe_filter.filter_by_ingredients(user_inputs["selected_ingredients"])
        recipe_filter.filter_by_nutrition(
            protein_min=user_inputs["protein_min"],
            carbs_min=user_inputs["carbs_min"],
            fat_max=user_inputs["fat_max"],
        )
        filtered_recipes = recipe_filter.get_filtered_recipes()
        st.session_state["filtered_recipes"] = filtered_recipes
        st.session_state["current_recipe_index"] = 0
        return filtered_recipes

    def display_results(self, user_inputs: dict) -> None:
        """
        Display the results based on filtered recipes.

        Parameters:
        ----------
        user_inputs : dict
            Dictionary containing user-selected filters.
        """
        if self.filtered_recipes.empty:
            self.logger.info("No recipes found. Showing suggestions.")
            self.handle_no_recipes(user_inputs)
        else:
            st.session_state["no_recipes_message"] = ""
            self.render_dashboard()

    def handle_no_recipes(self, user_inputs: dict) -> None:
        """
        Display suggestions when no recipes match the filters.

        Parameters:
        ----------
        user_inputs : dict
            Dictionary containing user-selected filters.
        """
        selected_ingredients = user_inputs["selected_ingredients"]
        visualizer = RecipeVisualizer(self.recipes_df, self.interactions_df)
        visualizer.render_no_recipes_suggestions(selected_ingredients)

    def display_dashboard_or_message(self) -> None:
        """
        Display the front page or the filtered recipes dashboard.
        """
        if self.filtered_recipes is None or self.filtered_recipes.empty:
            self.logger.info("Displaying the front page.")
            render_front_page()
        else:
            self.render_dashboard()

    def render_dashboard(self) -> None:
        """
        Render the dashboard for the filtered recipes.
        """
        self.logger.info("Rendering dashboard.")
        visualizer = RecipeVisualizer(self.recipes_df, self.interactions_df)
        visualizer.render_dashboard(self.filtered_recipes)

    def check_recipe_buttons_in_main(self, user_inputs: dict) -> None:
        """
        Check if any recipe button is clicked and update session state.

        Parameters:
        ----------
        user_inputs : dict
            Dictionary containing user-selected filters.
        """
        for recipe_id_key in st.session_state.keys():
            if recipe_id_key.startswith("recipe_") and st.session_state[recipe_id_key]:
                self.logger.info("Recipe button clicked: %s", recipe_id_key)

                recipe_id = int(recipe_id_key.split("_")[1])
                clicked_recipe = self.recipes_df[
                    self.recipes_df["id"] == recipe_id
                ].iloc[0]

                user_inputs["start_search"] = True
                user_inputs["selected_ingredients"] = clicked_recipe["ingredient_PP"]
                user_inputs["recipe_clicked"] = True

                st.session_state["filtered_recipes"] = self.recipes_df[
                    self.recipes_df["id"] == recipe_id
                ]

                for key in st.session_state.keys():
                    if key.startswith("recipe_"):
                        st.session_state[key] = False
                break


if __name__ == "__main__":
    app = RecipeApp()
    app.run()
