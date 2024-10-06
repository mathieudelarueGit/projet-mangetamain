import logging
import pandas as pd
import streamlit as st
from log_config import *
from data_loader import *

# Get a logger specific to this module
logger = logging.getLogger(__name__)

# EDA
def dataset_study(file_name: str) -> None:
    """
    Loads and analyzes a CSV file of recipes.

    Args:
        file_name (str): Path to the CSV file containing the recipe data.

    Returns:
        None: This function does not return a value. It prints the column names,
              data description, and the number of missing entries in the DataFrame.
    """
    # Calling the function load_data from the file data_loader
    df = load_data(file_name)
    
    # Print column names
    print("Column names:", df.columns)
    
    # Print data description
    print(df.describe())
    
    # Analyze missing data
    print("Number of missing data:", df.isnull().sum().sum())

def filtering_bio_recipes_kaggle() -> pd.DataFrame:
    """
    Filters out organic or traditional recipes based on tags.

    Args:
        None

    Returns:
        pd.DataFrame: A DataFrame containing only recipes with tags such as 
                      'vegan', 'bio', 'gluten-free', 'veggie', or 'organic'.
    
    Raises:
        ValueError: If the 'tags' column is not present in the DataFrame.
    """
    base_url = "https://www.kaggle.com/api/v1"
    owner_slug = "shuyangli94"
    dataset_slug = "food-com-recipes-and-user-interactions"
    dataset_version = "2"
    
    df_raw_recipes = load_data_kaggle(base_url, owner_slug, dataset_slug, dataset_version)
    print("Column names:", df_raw_recipes.columns)
    if 'tags' not in df_raw_recipes.columns:
        raise ValueError("The 'tags' column is missing from the DataFrame.")
    
    key_words_bio = r'\b(veggie|organic|bio)\b'
    
    # Filtering recipes with the tags bio, organic, traditional, gluten-free, veggie
    bio_recipes1 = df_raw_recipes[df_raw_recipes['tags'].str.contains(key_words_bio, case=False, na=False, regex=True)]
    print(bio_recipes1)
    return bio_recipes1

# Define the dataset slug and file names
filename_recipes = "dataset/PP_recipes.csv_extracted/PP_recipes.csv"
filename_users = "dataset/PP_users.csv_extracted/PP_users.csv"

# Uncomment the next line to perform dataset study
# data_recipes = dataset_study(filename_recipes)

bio_recipes = filtering_bio_recipes_kaggle()
