import streamlit as st


def get_sidebar_configurations(recipes_df, ingredient_list):
    """
    Define the sidebar configurations and return the user's inputs.
    """
    st.sidebar.title("What are we eating today?")

    # Initialize session state for expanders if not already set
    if "reset_clicked" not in st.session_state:
        st.session_state["reset_clicked"] = False
    if "expand_ingredients" not in st.session_state:
        st.session_state["expand_ingredients"] = False
    if "expand_macronutrients" not in st.session_state:
        st.session_state["expand_macronutrients"] = False

    # **Collapsible Section: Search by Ingredients**
    with st.sidebar.expander(
        "What's in your fridge?",
        expanded=st.session_state.get("expand_ingredients", False),
    ):
        # Use the widget's return value directly instead of modifying session state
        selected_ingredients = st.multiselect(
            "Type to search ingredients:",
            options=ingredient_list,
            default=st.session_state.get(
                "selected_ingredients", []
            ),  # Default value for the widget
            key="selected_ingredients",
            help="Start typing to see suggestions for ingredients.",
        )

        # Compact Display of Selected Ingredients
        if selected_ingredients:
            selected_summary = ", ".join(
                selected_ingredients[:3]
            )  # Show first 3 ingredients
            if len(selected_ingredients) > 3:
                selected_summary += f" + {len(selected_ingredients) - 3} more"
            st.caption(f"Selected Ingredients: {selected_summary}")
        else:
            st.caption("No ingredients selected.")

    # **Collapsible Section: Macronutrients**
    with st.sidebar.expander(
        "Macronutrients", expanded=st.session_state.get("expand_macronutrients", False)
    ):
        # Protein Slider
        protein_min = st.slider(
            "Minimum Protein (g)",
            min_value=0,
            max_value=150,
            value=st.session_state.get("protein_min", 0),
            step=1,
            key="protein_min",
        )

        # Carbs Slider
        carbs_min = st.slider(
            "Minimum Carbs (g)",
            min_value=0,
            max_value=300,
            value=st.session_state.get("carbs_min", 0),
            step=1,
            key="carbs_min",
        )

        # Fat Slider
        fat_max = st.slider(
            "Maximum Fat (g)",
            min_value=0,
            max_value=150,
            value=st.session_state.get("fat_max", 150),
            step=1,
            key="fat_max",
        )

        # Calculate total calories dynamically
        total_calories = (protein_min * 4) + (carbs_min * 4) + (fat_max * 9)
        st.markdown(f"**Total Calories: {total_calories} Kcal**")

    # **Buttons Below Expander**
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        reset_clicked = st.button("Start over", key="reset_button")
    with col2:
        start_search = st.button("Try My Luck!", key="start_search_button")

    # Handle reset button
    if reset_clicked:
        # Use st.session_state.clear() carefully without conflicting widget keys
        st.session_state.clear()  # Clears session state, but widgets will reinitialize
        st.rerun()  # Restart the app

    # Return all user inputs
    return {
        "selected_ingredients": selected_ingredients,  # Use widget return value
        "protein_min": protein_min,
        "carbs_min": carbs_min,
        "fat_max": fat_max,
        "start_search": start_search,
        "reset_clicked": reset_clicked,
        "total_calories": total_calories,
    }
