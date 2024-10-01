#!/usr/bin/python3.11
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd

# boutons: valeur graphe
# méthode appelée boutons streamlit fonctions appelées dans le fichier classes.py

from classes.classes import Functions

# Titre de la page
st.title("Hello World")


# Texte simple

st.write("Bienvenue sur votre première application Streamlit !")

df = pd.read_csv("data/PP_recipes.csv")
test_text_to_display = df.head().to_string()


st.write("Cliquez ici pour visualiser le dataframe sous: data/PP_recipes.csv")

# Ajouter un bouton interactif
if st.button("Cliquez ici pour visualiser le dataframe"):
    st.write(Functions.head_dataframe("data/P_recipes.csv"))
