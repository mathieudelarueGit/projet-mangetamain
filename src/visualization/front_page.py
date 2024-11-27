import streamlit as st


def render_front_page():
    """
    Render the front page of the app when no recipes are displayed.
    """
    # Add a banner image (use a relative path to assets directory)
    st.image(
        "src/visualization/images/mangetamain_front_page_banner.jpg",
        use_column_width=True,
    )

    # Welcome text with HTML for styling
    st.markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <h1>Welcome to Mangetamain!</h1>
            <p>
                A web app designed to help you cook healthy recipes
                depending on what is available in your fridge.
            </p>
            <p>
                At Mangetamain, you will only find traditional bio
                recipes that will make you healthier! We retrieved only recipes
                that our dear contributors rated minimum 4 stars,
                so you won't be disappointed!
            </p>
            <p>
                Just select which ingredients you have in your fridge,
                and we will propose you the best recipes there is for you.
                `You can even filter by macronutrients if you are on a specific diet
                or you just care about what's inside your plate!
            </p>
            <p>
                In doubt, you can always refer to the MTM score,
                an in-house score specifically designed to help
                you assess the quality of the recipe.
            </p>
            <h2>Have fun!</h2>
        </div>
    """,
        unsafe_allow_html=True,
    )
