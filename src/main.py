import pandas as pd
import streamlit as st

from data_loader import *

# Load data files into dataframes
df_PP_recipes = load_data("dataset/PP_recipes.csv.zip")
df_PP_users = load_data("dataset/PP_users.csv.zip")
df_ingredients = load_data("dataset/ingr_map.pkl")

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
