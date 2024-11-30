import streamlit as st
import pandas as pd

from src.visualization.sidebar import get_sidebar_configurations
from src.visualization.dashboard import RecipeVisualizer
from src.visualization.front_page import render_front_page

from src.data_loader import DataLoader
from src.filter import RecipeFilter


class RecipeApp:
    def __init__(self):
        # Initialize data
        self.data_loader = DataLoader()
        self.recipes_df, self.ingredient_list = self.data_loader.load_and_parse_data(
            "dataset/PP_recipes_final.csv.zip"
        )
        self.interactions_df = self.data_loader.load_data(
            "dataset/PP_interactions_final.csv.zip"
        )
        self.interactions_df["date"] = pd.to_datetime(self.interactions_df["date"])
        self.filtered_recipes = None

    def run(self):
        """Run the main logic of the app."""
        # Get user inputs from sidebar
        user_inputs = get_sidebar_configurations(self.recipes_df, self.ingredient_list)

        # Reset session state if reset is clicked
        if user_inputs["reset_clicked"]:
            self.reset_session_state()

        # Handle filtering and search
        if user_inputs["start_search"]:
            self.filtered_recipes = self.filter_recipes(user_inputs)
            self.display_results(user_inputs)
        else:
            self.filtered_recipes = st.session_state.get("filtered_recipes", None)
            self.display_dashboard_or_message()

    def reset_session_state(self):
        """Reset the app state."""
        render_front_page()
        st.session_state.clear()
        st.rerun()

    def filter_recipes(self, user_inputs):
        """Filter recipes based on user inputs."""
        recipe_filter = RecipeFilter(self.recipes_df)
        recipe_filter.filter_by_ingredients(user_inputs["selected_ingredients"])
        recipe_filter.filter_by_nutrition(
            protein_min=user_inputs["protein_min"],
            carbs_min=user_inputs["carbs_min"],
            fat_max=user_inputs["fat_max"],
        )
        filtered_recipes = recipe_filter.get_filtered_recipes()

        # Update session state with filtered recipes
        st.session_state["filtered_recipes"] = filtered_recipes
        st.session_state["current_recipe_index"] = 0  # Reset index
        return filtered_recipes

    def display_results(self, user_inputs):
        """Display results or suggestions based on filtered recipes."""
        if self.filtered_recipes.empty:
            self.handle_no_recipes(user_inputs)
        else:
            st.session_state["no_recipes_message"] = ""
            self.render_dashboard()

    def handle_no_recipes(self, user_inputs):
        """Handle cases where no recipes match the filters."""
        selected_ingredients = user_inputs["selected_ingredients"]
        visualizer = RecipeVisualizer(self.recipes_df, self.interactions_df)
        visualizer.render_no_recipes_suggestions(selected_ingredients)

    def display_dashboard_or_message(self):
        """Display the front page or the dashboard."""
        if self.filtered_recipes is None or self.filtered_recipes.empty:
            render_front_page()
        else:
            self.render_dashboard()

    def render_dashboard(self):
        """Render the dashboard with filtered recipes."""
        visualizer = RecipeVisualizer(self.recipes_df, self.interactions_df)
        visualizer.render_dashboard(self.filtered_recipes)


if __name__ == "__main__":
    app = RecipeApp()
    app.run()
