import streamlit as st
import pandas as pd

from data_loader import *

# Titre de la page
st.title("Hello World")

df_PP_recipes = load_data("dataset/PP_recipes.csv.zip")
st.write(df_PP_recipes.head())
