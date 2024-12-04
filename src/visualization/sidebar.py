import logging
import streamlit as st

# Create a logger for this module
logger = logging.getLogger(__name__)


def get_sidebar_configurations(recipes_df, ingredient_list) -> dict:
    """
    Define the sidebar configurations and return the user's inputs.

    Parameters:
    ----------
    recipes_df : pd.DataFrame
        The DataFrame containing recipe data.
    ingredient_list : list
        The list of available ingredients for selection.

    Returns:
    -------
    dict
        User inputs from the sidebar, including selected ingredients
        and macronutrient filters.
    """
    logger.info("Rendering sidebar configurations.")

    try:
        st.sidebar.title("What are we eating today?")

        # Initialize session state for expanders and buttons
        if "reset_clicked" not in st.session_state:
            st.session_state["reset_clicked"] = False
        if "expand_ingredients" not in st.session_state:
            st.session_state["expand_ingredients"] = False
        if "expand_macronutrients" not in st.session_state:
            st.session_state["expand_macronutrients"] = False

        # Collapsible Section: Search by Ingredients
        with st.sidebar.expander(
            "What's in your fridge?",
            expanded=st.session_state.get("expand_ingredients", False),
        ):
            selected_ingredients = st.multiselect(
                "Type to search ingredients:",
                options=ingredient_list,
                default=st.session_state.get("selected_ingredients", []),
                key="selected_ingredients",
                help="Start typing to see suggestions for ingredients.",
            )

            # Display selected ingredients in a compact format
            if selected_ingredients:
                selected_summary = ", ".join(selected_ingredients[:3])
                if len(selected_ingredients) > 3:
                    selected_summary += f" + {len(selected_ingredients) - 3} more"
                st.caption(f"Selected Ingredients: {selected_summary}")
            else:
                st.caption("No ingredients selected.")

        # Collapsible Section: Macronutrients
        with st.sidebar.expander(
            "Macronutrients",
            expanded=st.session_state.get("expand_macronutrients", False),
        ):
            # Macronutrient sliders
            protein_min = st.slider(
                "Minimum Protein (g)",
                min_value=0,
                max_value=150,
                value=st.session_state.get("protein_min", 0),
                step=1,
                key="protein_min",
            )
            carbs_min = st.slider(
                "Minimum Carbs (g)",
                min_value=0,
                max_value=300,
                value=st.session_state.get("carbs_min", 0),
                step=1,
                key="carbs_min",
            )
            fat_max = st.slider(
                "Maximum Fat (g)",
                min_value=0,
                max_value=150,
                value=st.session_state.get("fat_max", 150),
                step=1,
                key="fat_max",
            )

            # Display calculated total calories
            total_calories = (protein_min * 4) + (carbs_min * 4) + (fat_max * 9)
            st.markdown(f"**Total Calories: {total_calories} Kcal**")

        # Buttons Section
        st.sidebar.markdown("---")
        col1, col2 = st.sidebar.columns([1, 1])
        with col1:
            reset_clicked = st.button("Start over", key="reset_button")
        with col2:
            start_search = st.button("Try My Luck!", key="start_search_button")

        # Handle reset button
        if reset_clicked:
            logger.info("Reset button clicked, clearing session state.")
            st.session_state.clear()  # Clear session state and restart the app
            st.rerun()

        # Return all user inputs
        logger.info("User inputs collected successfully.")
        return {
            "selected_ingredients": selected_ingredients,
            "protein_min": protein_min,
            "carbs_min": carbs_min,
            "fat_max": fat_max,
            "start_search": start_search,
            "reset_clicked": reset_clicked,
            "recipe_clicked": False,
            "total_calories": total_calories,
        }
    except Exception as e:
        logger.error("Error while rendering sidebar: %s", str(e))
        raise
