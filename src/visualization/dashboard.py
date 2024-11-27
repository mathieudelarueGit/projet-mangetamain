import streamlit as st
import pandas as pd
from visualization.charts import ChartFactory
from metrics import calculate_mtm_score


class RecipeVisualizer:
    def __init__(self, recipes_df, interactions_df):
        """
        Initialize the visualizer with recipes and interactions data.
        """
        self.recipes_df = recipes_df
        self.interactions_df = interactions_df

    def render_navigation(self, filtered_recipes):
        """
        Render navigation arrows and recipe title.
        """
        left_arrow, title, right_arrow = st.columns([1, 6, 1])

        # Initialize current recipe index in session state
        if "current_recipe_index" not in st.session_state:
            st.session_state["current_recipe_index"] = 0

        # Update current recipe index on arrow click
        with left_arrow:
            if st.button("⬅️", key="prev_arrow"):
                st.session_state["current_recipe_index"] = (
                    st.session_state["current_recipe_index"] - 1
                ) % len(filtered_recipes)

        with right_arrow:
            if st.button("➡️", key="next_arrow"):
                st.session_state["current_recipe_index"] = (
                    st.session_state["current_recipe_index"] + 1
                ) % len(filtered_recipes)

        # Display Recipe Title
        current_recipe = filtered_recipes.iloc[st.session_state["current_recipe_index"]]
        with title:
            st.markdown(
                f"<h3 style='text-align: center;'>{current_recipe['name']}</h3>",
                unsafe_allow_html=True,
            )

        return current_recipe

    def render_pie_chart(self, selected_recipe):
        """
        Render a pie chart for the selected recipe's macronutrient breakdown.
        """
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

    def render_popularity_chart(self, selected_recipe):
        """
        Render a popularity chart for the selected recipe.
        """
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

    def render_score_chart(self, selected_recipe):
        """
        Render the MTM Score as a custom visualization.
        """
        # mtm_score = calculate_mtm_score(selected_recipe["nutrition"])

        fig_score = ChartFactory.score_display(
            selected_recipe["mtm_score"], selected_recipe["nutrition"]
        )
        st.plotly_chart(
            fig_score, use_container_width=True, config={"displayModeBar": False}
        )

    def render_dashboard(self, filtered_recipes):
        """
        Render the complete dashboard for the selected recipe.
        """
        # Render navigation and get the current recipe
        current_recipe = self.render_navigation(filtered_recipes)

        # Display Pie Chart and Popularity Chart Side by Side
        # col1, col2, col3 = st.columns(3)
        col1, col2 = st.columns(2)

        with col1:
            self.render_score_chart(current_recipe)

        with col2:
            self.render_pie_chart(current_recipe)

        # with col3:
        # self.render_popularity_chart(current_recipe)
