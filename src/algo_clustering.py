import logging
import pandas as pd
import streamlit as st
from log_config import *
from data_loader import *
import kaggle


# Get a logger specific to this module
logger = logging.getLogger(__name__)

#EDA
def dataset_study(file_name: str) ->  None:
    #calling to the function load_data from the file data_loader
    df=load_data(file_name)
    """
    Loads and analyses a CSV file of recipes.

    Args:
        file_name (str): Path to the CSV file containing the recipe data.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    #column names
    print("Column names:", df.columns)
    #data description 
    print(df.describe())
    #étude des données manquantes
    print("Number of missing data:", df.isnull().sum().sum())
    

def filtering_bio_recipes(df: pd.DataFrame)-> pd.DataFrame:
    """
    Filters out organic or traditional recipes based on tags.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.

    Returns:
        pd.DataFrame: A DataFrame containing only recipes with tags such as organic’, ‘veggie’, ‘organic’, ‘traditional’, or ‘gluten-free’.

    """
    df=load_data(df)
    features_bio = r'\b(bio|veggie|organic|gluten-free|vegan)\b'
    # filtering recipes with the tags bio, organic, traditional, gluten-free, veggie
    #bio_recipes= df[df['tags'].str.contains(features_bio, case=False, na=False, regex=True)]
    key_words = ['vegan', 'bio', 'gluten-free', 'veggie','organic']
    #show the lines where lines of bio_recipes have these key_words
    bio_recipes1 = df[df['tags'].isin(key_words)]
    bio_recipes_list=bio_recipes1["id","name"]
    return bio_recipes_list


# Définir le slug du dataset et le nom du fichier
dataset_slug = 'shuyangli94/food-com-recipes-and-user-interactions'
filename = 'RAW_recipes.csv'

# Charger le dataset
#df = load_kaggle_dataset(dataset_slug, filename)

filename_recipes="dataset/PP_recipes.csv_extracted/PP_recipes.csv"
filename_users="dataset/PP_users.csv_extracted/PP_users.csv"
temporary_filename_raw="/RAW_recipes.csv"
data_recipes=dataset_study(filename_recipes)
#data_users=dataset_study(filename_users)
#df_bio=filtering_bio_recipes(temporary_filename_raw)
#print(df_bio)













