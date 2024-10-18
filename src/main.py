import logging
import streamlit as st

from data_loader import load_data
from log_config import setup_logging

# Initialize logging
setup_logging()

# Get a logger specific to this module
logger = logging.getLogger(__name__)

# Load data files into dataframes
df_PP_recipes = load_data("dataset/PP_recipes.csv.zip")
df_PP_users = load_data("dataset/PP_users.csv.zip")
df_ingredients = load_data("dataset/ingr_map.pkl")
df_RAW_recipes = load_data("dataset/RAW_recipes.csv.zip")
df_RAW_interactions = load_data("dataset/RAW_interactions.csv.xz")

# Title
st.write("Bienvenue sur notre nouvelle app Streamlit!")

# Provide file options in a selectbox
file_options = ["Recettes", "Recettes brutes", "Utilisateurs", "Ingrédients", "Interactions utilisateurs"]
dataframes = {
    "Recettes": df_PP_recipes,
    "Recettes brutes": df_RAW_recipes,
    "Interactions utilisateurs": df_RAW_interactions,
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
