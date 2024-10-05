import logging
import pandas as pd
import streamlit as st
from log_config import *

# Get a logger specific to this module
logger = logging.getLogger(__name__)

#EDA
def dataset_recipes_study(file_name: str) ->  pd.DataFrame:
    """
    Loads and analyses a CSV file of recipes.

    Args:
        file_name (str): Path to the CSV file containing the recipe data.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    df=pd.read_csv(file_name,sep="," )
    #noms des colonnes
    print(df.columns)
    #description des données
    print(df.describe())
    print(df.dropna)
    #étude des données manquantes
    print(df.isnull().sum().sum())#0 données manquantes
    return df

def filtering_bio_recipes(df: pd.DataFrame)-> pd.DataFrame:
    """
    Filters out organic or traditional recipes based on tags.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.

    Returns:
        pd.DataFrame: A DataFrame containing only recipes with tags such as organic’, ‘veggie’, ‘organic’, ‘traditional’, or ‘gluten-free’.

    """
    features_bio = r'\b(bio|veggie|organic|traditional|gluten-free)\b'
    # Filtrer les recettes avec les tags 'bio' ou 'traditionnel'
    bio_recipes= df[df['tags'].str.contains(features_bio, case=False, na=False, regex=True)]
    return bio_recipes

#df_bio=filtering_bio_recipes(df)
#print(df_bio)













