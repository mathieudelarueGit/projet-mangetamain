import streamlit as st
from src.visualization.charts import ChartFactory


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
            pie_fig,
            use_container_width=True,
            config={"displayModeBar": False},
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
            st.plotly_chart(
                fig_popularity,
                use_container_width=True,
            )

    def render_score_chart(self, selected_recipe):
        """
        Render the MTM Score as a custom visualization.
        """
        fig_score = ChartFactory.score_display(
            selected_recipe["mtm_score"], selected_recipe["nutrition"]
        )
        st.plotly_chart(
            fig_score,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    def render_dashboard(self, filtered_recipes):
        """
        Render the complete dashboard for the selected recipe.
        """
        # Render navigation and get the current recipe
        current_recipe = self.render_navigation(filtered_recipes)

        # Display Pie Chart and Popularity Chart Side by Side
        col1, col2 = st.columns(2)

        with col1:
            self.render_score_chart(current_recipe)

        with col2:
            self.render_pie_chart(current_recipe)

    def render_no_recipes_suggestions(self, selected_ingredients):
        """
        Render suggestions when no recipes match the user's criteria.
        """
        st.session_state["no_recipes_message"] = (
            "We didn't find any recipes that match your criteria. "
            "Here are some suggestions based on your selected ingredients. "
            "Consider adding the missing ingredients!"
        )

        # Find recipes with matching ingredients
        matching_recipes = self.recipes_df[
            self.recipes_df["ingredient_PP"].apply(
                lambda ingredients: all(
                    selected in ingredients for selected in selected_ingredients
                )
            )
        ]

        # Select up to 5 random recipes
        random_recipes = matching_recipes.sample(min(5, len(matching_recipes)))

        # Display a styled header for the suggestions
        st.markdown(
            "<h2 style='color:#FF6347;'>🔍 Suggestions Based on Your Ingredients</h2>",
            unsafe_allow_html=True,
        )
        st.write(st.session_state["no_recipes_message"])

        # Display each recipe suggestion with mtm_score and missing ingredients
        for _, recipe in random_recipes.iterrows():
            with st.container():
                # Recipe name without anchor link
                st.markdown(
                    f"<p style='font-size:24px; color:#4682B4; margin-bottom:0;'>"
                    f"{recipe['name']}</p>",
                    unsafe_allow_html=True,
                )

                # MTM score and missing ingredients logic remains the same
                mtm_score = recipe["mtm_score"]
                if mtm_score < 30:
                    score_color = "#FF0000"  # Red
                elif 30 <= mtm_score < 70:
                    score_color = "#FFA500"  # Orange
                else:
                    score_color = "#2E8B57"  # Green

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
                if missing_ingredients:
                    st.markdown(
                        f"<p><strong>Missing Ingredients:</strong> "
                        f"{', '.join(missing_ingredients)}</p>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        "<p><strong>Missing Ingredients:</strong> None</p>",
                        unsafe_allow_html=True,
                    )

                # Add a separator between recipes
                st.markdown(
                    "<hr style='border:1px solid #DCDCDC;'>",
                    unsafe_allow_html=True,
                )
