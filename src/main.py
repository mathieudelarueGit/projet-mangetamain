import streamlit as st
import pandas as pd

from src.visualization.sidebar import get_sidebar_configurations
from src.visualization.dashboard import RecipeVisualizer
from src.visualization.front_page import render_front_page

from src.data_loader import DataLoader
from src.filter import RecipeFilter

# Load data
data_loader = DataLoader()
# recipes_df, ingredient_list = data_loader.load_recipes()
# interactions_df = data_loader.load_interactions()

recipes_df, ingredient_list = data_loader.load_and_parse_data(
    "dataset/PP_recipes_final.csv.zip"
)
# recipes_df = data_loader.load_data("dataset/PP_recipes_final.csv.zip")
interactions_df = data_loader.load_data("dataset/PP_interactions_final.csv.zip")
interactions_df["date"] = pd.to_datetime(interactions_df["date"])

print(f"Nb ingredients uniques: {len(ingredient_list)}")

# Sidebar filters
user_inputs = get_sidebar_configurations(recipes_df, ingredient_list)

print(user_inputs)
print(f"Session state: {st.session_state}")
# If reset is clicked, clear session state
if user_inputs["reset_clicked"]:
    print("Entering here")
    print(f"Session state: {st.session_state}")
    render_front_page()
    st.rerun()
    st.stop()

# FILTERING
if user_inputs["start_search"]:
    # Initialize RecipeFilter
    recipe_filter = RecipeFilter(recipes_df)

    # Apply ingredient filter
    recipe_filter.filter_by_ingredients(user_inputs["selected_ingredients"])

    # Apply nutrition filters
    recipe_filter.filter_by_nutrition(
        protein_min=user_inputs["protein_min"],
        carbs_min=user_inputs["carbs_min"],
        fat_max=user_inputs["fat_max"],
    )

    # Store the filtered recipes in session state
    filtered_recipes = recipe_filter.get_filtered_recipes()
    st.session_state["filtered_recipes"] = filtered_recipes
    st.session_state["current_recipe_index"] = 0  # Reset to the first recipe

    # Handle "No Recipes Found" case
    if filtered_recipes.empty:
        st.session_state["no_recipes_message"] = (
            "We didn't find any recipes that match your criteria. "
            "Try adding more ingredients or "
            " choose a different combination of macronutrients!"
        )
    else:
        st.session_state["no_recipes_message"] = ""

else:
    # Retrieve filtered recipes from session state
    filtered_recipes = st.session_state.get("filtered_recipes", None)

# DASHBOARD
if filtered_recipes is None or filtered_recipes.empty:
    # Display front page or "No Recipes Found" message
    if (
        "no_recipes_message" in st.session_state
        and st.session_state["no_recipes_message"]
    ):
        st.sidebar.markdown(
            f"<span style='color:red;'>{st.session_state['no_recipes_message']}</span>",
            unsafe_allow_html=True,
        )
    else:
        render_front_page()
else:
    # Initialize RecipeVisualizer
    visualizer = RecipeVisualizer(recipes_df, interactions_df)
    visualizer.render_dashboard(filtered_recipes)
