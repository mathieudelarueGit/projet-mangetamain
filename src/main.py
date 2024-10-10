import logging
import streamlit as st

from data_loader import load_data  # Explicit import
from log_config import setup_logging  # Explicit import

# Initialize logging
setup_logging()

# Get a logger specific to this module
logger = logging.getLogger(__name__)

# Load data files into dataframes
df_PP_recipes = load_data("dataset/PP_recipes.csv.zip")
df_PP_users = load_data("dataset/PP_users.csv.zip")
df_ingredients = load_data("dataset/ingr_map.pkl")
df_RAW_recipes = load_data("dataset/RAW_recipes.csv.zip")

# Title
st.write("Bienvenue sur l'application Streamlit de Mangetamain!")

# Provide file options in a selectbox
file_options = ["Recettes", "Utilisateurs", "Ingrédients"]
dataframes = {
    "Recettes": df_PP_recipes,
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
