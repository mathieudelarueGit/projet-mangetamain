import os
print("Répertoire de travail main :", os.getcwd())

import logging
import streamlit as st

# Set the page layout to full width, needs to be at the beginning of the script
st.set_page_config(layout="wide") # Needs to be at the beginning of the script

# Explicit imports of home-made modules and features
from data_loader import load_data  
from log_config import setup_logging 
from graphs import fig1, fig2, fig3, top10_hottest_recipes 

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
st.write("Welcome into Mangetamain! data exploration & analysis project")

# Layout for columns
row1_1, row1_2, row1_3, row1_4 = st.columns((3, 2, 2, 4))

with row1_1:
    st.write("## Encyclopedia for foodies")
    st.write(f"Number of recipes: {df_RAW_recipes.shape[0]}")

with row1_2:
    st.write("## Wide community")
    st.write(f"As many as {df_PP_users.shape[0]} users got their hands dirty and shared their recipes")

with row1_3:
    st.write("## Varied food")
    st.write(f"{df_ingredients.shape[0]} different ingredients are found")

with row1_4:
    font_size = 2
    st.write("## Most popular recipes")
    st.write(f"<font size={font_size}>Some recipes are too popular to be serious: \n {top10_hottest_recipes}</font>", unsafe_allow_html=True)

# Second row of columns for graphs
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
