import logging

import streamlit as st

# Set the page layout to full width, needs to be at the beginning of the script
st.set_page_config(layout="wide")  # Needs to be at the beginning of the script

from data_loader import DataLoader
from log_config import setup_logging
from utils import df_filtered_bio, rate_bio_recipes
from visualisation.graphs import fig1, fig2, fig3, top10_hottest_recipes
from visualisation.graphs_nutrition import categories, nutrition_hist


# Initialize logging
setup_logging()

# Get a logger specific to this module
logger = logging.getLogger(__name__)

# Instantiate the DataLoader
data_loader = DataLoader()

# Load data files into dataframes
df_PP_recipes = data_loader.load_data("dataset/PP_recipes.csv.zip")
df_PP_users = data_loader.load_data("dataset/PP_users.csv.zip")
df_ingredients = data_loader.load_data("dataset/ingr_map.pkl")
df_RAW_recipes = data_loader.load_data("dataset/RAW_recipes.csv.zip")
# Not used here, comment out as req :
# df_RAW_interactions = data_loader.load_data("dataset/RAW_interactions.csv.xz")


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
        st.write(f"Number of recipes: {df_RAW_recipes.shape[0]}")
        st.write(
            f"Number of bio recipes: {df_filtered_bio.shape[0]:,}".replace(",", " ")
        )
        st.write(f"Proportion of bio recipes: {rate_bio_recipes:.2f}%")

    with row1_2:
        st.write(
            "As many as {} users got their hands dirty and shared their recipes".format(
                df_PP_users.shape[0]
            )
        )

    with row1_3:
        st.write(f"{df_ingredients.shape[0]} different ingredients are found")

    with row1_4:
        font_size = 2
        st.write(
            f"<font size={font_size}>{top10_hottest_recipes}</font>",
            unsafe_allow_html=True,
        )

    # Sidebar
    st.sidebar.title("“This is the sidebar”")  ## TO DO
    st.sidebar.markdown(
        "“Let’s start with binary and non-binary classification!!”"
    )  ## TO DO

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

        st.sidebar.subheader("Choose classifier")  # Add a subheader to the sidebar

    classifier = st.sidebar.selectbox(
        "Classifier",  # Add a selectbox to the sidebar
        (
            "Support Vector Machine (SVM)",  ## TO DO: Add real classifiers
            "Logistic Regression",  ## TO DO: Add real classifiers
            "Random Forest",
        ),
    )  ## TO DO: Add real classifiers

    if classifier == "Support Vector Machine (SVM)":
        st.sidebar.subheader("Hyperparameters")
        st.subheader(
            "Here are the hyperparameters for SVM"
        )  ## TO DO: add real features
        C = st.sidebar.number_input(
            "C (Regularization parameter)", 0.01, 10.0, step=0.01, key="C"
        )
        kernel = st.sidebar.radio("Kernel", ("rbf", "linear"), key="kernel")
        gamma = st.sidebar.radio(
            "Gamma (Kernal coefficient", ("scale", "auto"), key="gamma"
        )
        metrics = st.sidebar.multiselect(
            "What metrics to plot?",
            ("Confusion Matrix", "ROC Curve", "Precision-Recall Curve"),
        )
        st.write(f"kernel: {kernel}, C: {C}, gamma: {gamma}, metrics: {metrics}")
    # Provide file options in a selectbox

    file_options = ["Recettes", "Recettes brutes", "Utilisateurs", "Ingrédients"]
    dataframes = {
        "Recettes": df_PP_recipes,
        "Recettes brutes": df_RAW_recipes,
        "Utilisateurs": df_PP_users,
        "Ingrédients": df_ingredients,
    }
    selected_file = st.selectbox(
        "Quel dataframe souhaitez-vous séléctionner: ", file_options
    )

    # Add a button to trigger file loading and display
    if st.button("Afficher le dataframe"):
        st.write(f"Data du dataframe: {selected_file}")
        df = dataframes[selected_file]
        st.write(df.head())


if __name__ == "__main__":
    main()  # this prevents the code from running when the module is imported
