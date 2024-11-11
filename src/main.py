import streamlit as st
st.set_page_config(layout="wide")
from data_loader import DataLoader
from log_config import setup_logging
from utils import (
    df_preprocessed,
    rate_bio_recipes,
    outliers_zscore_df,
)
from visualisation.graphs import fig1, fig2, fig3, top10_hottest_recipes
from visualisation.graphs_nutrition import categories, nutrition_hist

# Initialize logging and set page configuration
setup_logging()
# Use session state to avoid reloading data multiple times
if "data_loader" not in st.session_state:
    st.session_state.data_loader = DataLoader()


# Load data files once using caching
@st.fragment
def load_data_files():
    data_loader = st.session_state.data_loader
    df_PP_users = data_loader.load_data("dataset/PP_users.csv.zip")
    df_ingredients = data_loader.load_data("dataset/ingr_map.pkl")
    return df_PP_users, df_ingredients


df_PP_users, df_ingredients = load_data_files()


@st.fragment
def display_title():
    """Displays the main title of the project"""
    st.write("Welcome into Mangetamain! data exploration & analysis project")


@st.fragment
def display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df):
    """Displays the key statistics using st.metric widgets"""
    row0_1, row0_2, row0_3, row0_4 = st.columns((3, 2, 2, 4))

    with row0_1:
        st.write("## Encyclopedia for foodies")
    with row0_2:
        st.write("## Wide community")
    with row0_3:
        st.write("## Varied food")
    with row0_4:
        st.write("## Most popular recipes")

    row1_1, row1_2, row1_3, row1_4 = st.columns((3, 2, 2, 4))

    with row1_1:
        st.metric(
            label="Bio recipes",
            value=f"{df_preprocessed.shape[0]:,}".replace(",", " "),
            help="Number of bio recipes after pre-processing",
        )
        st.metric("Bio recipes proportion (%)", f"{rate_bio_recipes:.2f}%")
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
        st.write(f"{top10_hottest_recipes}", unsafe_allow_html=True)


@st.fragment
def display_general_aspects():
    """Displays general analysis charts"""
    row2_1, row2_2, row2_3 = st.columns(3)

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


@st.fragment
def display_nutritional_analysis():
    """Displays a dropdown and chart for nutritional components analysis"""
    st.title("Top 5 Recipes per nutritional component")
    selected_category = st.selectbox("Select a nutritional component", categories)
    st.plotly_chart(nutrition_hist[selected_category])


def main():
    display_title()
    display_statistics(df_preprocessed, rate_bio_recipes, outliers_zscore_df)
    # Sidebar setup
    st.sidebar.title("“This is the sidebar”")
    if st.sidebar.checkbox("Show general aspects", True):
        st.subheader("Some general purpose analysis")
        display_general_aspects()

    # Displaying nutritional components
    display_nutritional_analysis()


if __name__ == "__main__":
    main()
