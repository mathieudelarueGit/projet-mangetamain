import ast
import datetime
import gc
import logging

import pandas as pd
import streamlit as st
from src.visualization.charts import ChartFactory

# Create a logger for the RecipeVisualizer module
logger = logging.getLogger(__name__)


class RecipeVisualizer:
    """
    A class for visualizing recipes and related data in the Streamlit app.
    """

    def __init__(self, recipes_df: pd.DataFrame, interactions_df: pd.DataFrame) -> None:
        """
        Initialize the visualizer with recipe and interaction data.

        Parameters:
        ----------
        recipes_df : pd.DataFrame
            DataFrame containing recipe data.
        interactions_df : pd.DataFrame
            DataFrame containing user interaction data.
        """
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df
        logger.info("RecipeVisualizer initialized with recipes and interactions data.")

    def render_navigation(self, filtered_recipes: pd.DataFrame) -> pd.Series:
        """
        Render navigation arrows and display the recipe title.
        Selects recipes based on the date of the user.

        Parameters:
        ----------
        filtered_recipes : pd.DataFrame
            DataFrame containing filtered recipes.

        Returns:
        -------
        pd.Series
            The current recipe being displayed.
        """

        # Select recipes based on the date of the user
        current_date = int(datetime.date.today().month)
        current_date += int(datetime.date.today().day) / 30 - 1
        # Obtain trough the data analysis
        std_dev = 1.54
        # Sets the filter for the recipes
        season_min = (current_date - std_dev) % 12
        season_max = (current_date + std_dev) % 12
        final = filtered_recipes.copy()
        # Conditions to limits requires some special care
        if season_min < 0:
            final[(final.avg_date > 12 + season_min) & (final.avg_date < season_max)]
        if season_max > 12:
            final[(final.avg_date > season_min) | (final.avg_date < season_max - 12)]
        else:
            final[(final.avg_date > season_min) & (final.avg_date < season_max)]
        # The case where no recipes are available
        if not final.empty:
            filtered_recipes = final
        # Freeing memory
        else:
            del final
            gc.collect()

        try:
            left_arrow_box, title, right_arrow_box = st.columns([1, 6, 1])

            if "current_recipe_index" not in st.session_state:
                st.session_state["current_recipe_index"] = 0

            with left_arrow_box:
                if st.button("", key="prev_arrow", icon=":material/arrow_circle_left:"):
                    st.session_state["current_recipe_index"] = (
                        st.session_state["current_recipe_index"] - 1
                    ) % len(filtered_recipes)

            with right_arrow_box:
                if st.button(
                    "", key="next_arrow", icon=":material/arrow_circle_right:"
                ):
                    st.session_state["current_recipe_index"] = (
                        st.session_state["current_recipe_index"] + 1
                    ) % len(filtered_recipes)

            current_recipe = filtered_recipes.iloc[
                st.session_state["current_recipe_index"]
            ]
            with title:
                st.markdown(
                    f"<h3 style='text-align: center;'>{current_recipe['name']}</h3>",
                    unsafe_allow_html=True,
                )
            logger.info("Rendered navigation for recipe: %s", current_recipe["name"])
            return current_recipe
        except Exception as e:
            logger.error("Failed to render navigation: %s", str(e))
            raise

    def render_pie_chart(self, selected_recipe: pd.Series) -> None:
        """
        Render a pie chart for the selected recipe's macronutrient breakdown.

        Parameters:
        ----------
        selected_recipe : pd.Series
            The selected recipe data.
        """
        try:
            macronutrient_values = [
                selected_recipe["nutrition"][1] * 9,  # Fat
                selected_recipe["nutrition"][4] * 4,  # Protein
                selected_recipe["nutrition"][6] * 4,  # Carbs
            ]
            macronutrient_labels = ["Fat", "Protein", "Carbs"]
            pie_fig = ChartFactory.pie_chart(
                macronutrient_labels, macronutrient_values, "Macronutrient Breakdown"
            )
            st.plotly_chart(
                pie_fig, use_container_width=True, config={"displayModeBar": False}
            )
            logger.info("Rendered pie chart for recipe: %s", selected_recipe["name"])
        except Exception as e:
            logger.error("Failed to render pie chart: %s", str(e))
            raise

    def render_popularity_chart(self, selected_recipe: pd.Series) -> None:
        """
        Render a popularity chart for the selected recipe.

        Parameters:
        ----------
        selected_recipe : pd.Series
            The selected recipe data.
        """
        try:
            recipe_interactions = self.interactions_df[
                self.interactions_df["recipe_id"] == selected_recipe["id"]
            ]
            if not recipe_interactions.empty:
                interactions_count = (
                    recipe_interactions.groupby("date")
                    .size()
                    .reset_index(name="Interactions")
                )
                fig_popularity = ChartFactory.popularity_chart(
                    interactions_count, "date", "Interactions"
                )
                st.plotly_chart(fig_popularity, use_container_width=True)
                logger.info(
                    "Rendered popularity chart for recipe: %s",
                    selected_recipe["name"],
                )
        except Exception as e:
            logger.error("Failed to render popularity chart: %s", str(e))
            raise

    def render_score_chart(self, selected_recipe: pd.Series) -> None:
        """
        Render the MTM Score as a custom visualization.

        Parameters:
        ----------
        selected_recipe : pd.Series
            The selected recipe data.
        """
        try:
            fig_score = ChartFactory.score_display(
                selected_recipe["mtm_score"], selected_recipe["nutrition"]
            )
            st.plotly_chart(
                fig_score, use_container_width=True, config={"displayModeBar": False}
            )
            logger.info("Rendered score chart for recipe: %s", selected_recipe["name"])
        except Exception as e:
            logger.error("Failed to render score chart: %s", str(e))
            raise

    def render_dashboard(self, filtered_recipes: pd.DataFrame) -> None:
        """
        Render the complete dashboard for the selected recipe.

        Parameters:
        ----------
        filtered_recipes : pd.DataFrame
            DataFrame containing filtered recipes.
        """
        try:
            current_recipe = self.render_navigation(filtered_recipes)

            col1, col2 = st.columns(2)
            with col1:
                self.render_score_chart(current_recipe)
            with col2:
                self.render_pie_chart(current_recipe)

            separtor = """
            ________________________________________________________________________
            """
            st.write(separtor)
            st.header("Now, let's cook!")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Just follow the steps**")
            with col2:
                show_ingredients = st.toggle(
                    "I wana see ingredients!", key="ingredients"
                )
            if show_ingredients:
                try:
                    for stuff in current_recipe["ingredient_PP"]:
                        st.write(f" - {stuff}")
                except BaseException:
                    st.write("No ingredients available")
                    logger.error(
                        "Failed to find ingredients: %s", current_recipe["name"]
                    )
                st.write(separtor)
            try:
                steps = ast.literal_eval(current_recipe["steps"])
                for step in steps:
                    st.write(f" - {step}")
            except BaseException:
                st.write("No steps available")
                logger.error("Failed to find steps: %s", current_recipe["name"])
            st.write(separtor)

            logger.info("Rendered dashboard for recipe: %s", current_recipe["name"])
        except Exception as e:
            logger.error("Failed to render dashboard: %s", str(e))
            raise

    def render_no_recipes_suggestions(self, selected_ingredients: list) -> None:
        """
        Render suggestions when no recipes match the user's criteria.

        Parameters:
        ----------
        selected_ingredients : list
            List of ingredients selected by the user.
        """
        try:
            st.session_state["no_recipes_message"] = (
                "We didn't find any recipes that match your criteria. "
                "Here are some suggestions based on your selected ingredients. "
                "Consider adding the missing ingredients!"
            )

            matching_recipes = self.recipes_df[
                self.recipes_df["ingredient_PP"].apply(
                    lambda ingredients: all(
                        selected in ingredients for selected in selected_ingredients
                    )
                )
            ]
            top_recipes = matching_recipes.nlargest(5, "mtm_score")

            st.markdown(
                "<h2 style='color:#FF6347;'>"
                "🔍 Suggestions Based on Your Ingredients</h2>",
                unsafe_allow_html=True,
            )
            st.write(st.session_state["no_recipes_message"])

            for _, recipe in top_recipes.iterrows():
                with st.container():
                    if st.button(
                        f"View Recipe: {recipe['name']}", key=f"recipe_{recipe['id']}"
                    ):
                        st.session_state[f"recipe_{recipe['id']}"] = True

                    mtm_score = recipe["mtm_score"]
                    score_color = (
                        "#FF0000"
                        if mtm_score < 30
                        else "#FFA500" if mtm_score < 70 else "#2E8B57"
                    )
                    st.markdown(
                        f"<p style='color:{score_color};'><strong>MTM Score:</strong> "
                        f"{mtm_score:.2f}</p>",
                        unsafe_allow_html=True,
                    )

                    missing_ingredients = [
                        ingredient
                        for ingredient in recipe["ingredient_PP"]
                        if ingredient not in selected_ingredients
                    ]
                    missing = (
                        ", ".join(missing_ingredients)
                        if missing_ingredients
                        else "None"
                    )
                    st.markdown(
                        f"<p><strong>Missing Ingredients:</strong> {missing}</p>",
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        "<hr style='border:1px solid #DCDCDC;'>", unsafe_allow_html=True
                    )
            logger.info("Rendered no-recipes suggestions.")
        except Exception as e:
            logger.error("Failed to render no-recipes suggestions: %s", str(e))
            raise
