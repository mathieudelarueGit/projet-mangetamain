import logging

import streamlit as st

# Set the page layout to full width, needs to be at the beginning of the script
st.set_page_config(layout="wide")  # Needs to be at the beginning of the script

from data_loader import DataLoader
from log_config import setup_logging
from utils import (
    df_preprocessed,
    rate_bio_recipes,
    outliers_zscore_df,
)
from visualisation.graphs import fig1, fig2, fig3, top10_hottest_recipes
from visualisation.graphs_nutrition import categories, nutrition_hist


# Initialize logging
setup_logging()

# Get a logger specific to this module
logger = logging.getLogger(__name__)

# Instantiate the DataLoader
data_loader = DataLoader()

# Load data files into dataframes
df_PP_users = data_loader.load_data("dataset/PP_users.csv.zip")
df_ingredients = data_loader.load_data("dataset/ingr_map.pkl")


def main() -> None:
    """_summary_: this function displays of the main page of the project"""
    # Title
    st.write("Welcome into Mangetamain! data exploration & analysis project")

    # Layout for columns
    row0_1, row0_2, row0_3, row0_4 = st.columns((3, 2, 2, 4))

    # A few statistics
    # Titles
    with row0_1:
        st.write("## Encyclopedia for foodies")
    with row0_2:
        st.write("## Wide community")
    with row0_3:
        st.write("## Varied food")
    with row0_4:
        font_size = 2
        st.write("## Most popular recipes")

    # A few statistics
    # Fully aligned statistics
    row1_1, row1_2, row1_3, row1_4 = st.columns((3, 2, 2, 4))

    with row1_1:
        # Total number of bio recipes
        st.metric(
            label="Bio recipes",
            value=f"{df_preprocessed.shape[0]:,}".replace(",", " "),
            help="Number of bio recipes after pre-processing",
        )
        st.metric("Bio recipes proportion (%)", f"{rate_bio_recipes:,}%")
        # Outliers proportion and number
        st.metric(
            label="Outliers",
            value=f"{len(outliers_zscore_df)}",
            help="Outliers count in bio recipes",
        )

    with row1_2:
        st.metric(
            label="Number of users",
            value=f"{df_PP_users.shape[0]:,}".replace(",", " "),
            help="As many as users got their hands dirty and shared their recipes",
        )

    with row1_3:
        st.metric(
            label="Ingredients",
            value=f"{df_ingredients.shape[0]:,}".replace(",", " "),
            help="Number of different ingredients found in the dataset",
        )

    with row1_4:
        font_size = 2
        st.write(
            f"<font size={font_size}>{top10_hottest_recipes}</font>",
            unsafe_allow_html=True,
        )

    # Sidebar
    st.sidebar.title("“This is the sidebar”")  ## TO DO

    # Shows if checkbox is checked, because it's slowing down the app
    if st.sidebar.checkbox(
        "Show general aspects", True
    ):  # Add a checkbox to display into the main page
        st.subheader("Some general purpose analysis")  ## TO DO

        # Second row of columns for graphs
        row2_1, row2_2, row2_3 = st.columns(3)

        # Display the graphs
        with row2_1:
            st.write("Most recipes are strongly rated:")
            st.plotly_chart(fig1)
            st.write("...hence rate will not be a good feature for recommendation.")
        with row2_2:
            st.write("The website and the database was burning hot until 2011:")
            st.plotly_chart(fig2)
            st.write("...from that point on, Instagram probably took over.")
        with row2_3:
            st.write("Some recipes are too popular to be serious:")
            st.plotly_chart(fig3)
            st.write("...but we'll keep away from them as they might be biased.")
        # TO DO: Add real classifiers
        # Create a dropdown for the user to select the category
        st.title("Top 5 Recipes per nutritionnal component")
        # Créer une liste déroulante (selectbox) pour sélectionner la catégorie
        selected_category = st.selectbox("Select a nutritional component", categories)
        # Afficher le graphique correspondant à la catégorie sélectionnée
        st.plotly_chart(nutrition_hist[selected_category])


if __name__ == "__main__":
    main()  # this prevents the code from running when the module is imported
