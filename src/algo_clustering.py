import logging
import pandas as pd
import numpy as np
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
    return df


def filtering_bio_recipes_kaggle(key_words_bio: str) -> pd.DataFrame:
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
    file_name="RAW_recipes.csv"

    df_raw_recipes = load_data_kaggle(base_url, owner_slug, dataset_slug, dataset_version, file_name)
    #key_words_bio = r'\b(gluten-free|dairy-free|organic|bio|vegetarian|veggie)\b'
    # Filtering recipes with the tags bio, organic, traditional, gluten-free, veggie
    bio_recipes1 = df_raw_recipes[df_raw_recipes['tags'].str.contains(key_words_bio, case=False, na=False, regex=True)]
    print("Nutritional information for bio recipes :")
    print(bio_recipes1["nutrition"].describe())  #displaying statisical description of the columns
    print(bio_recipes1)
    return bio_recipes1

def correlation_bio_recipes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the Pearson correlation matrix for the given DataFrame.

    This function computes the Pearson correlation coefficient between all 
    pairs of columns in the input DataFrame and returns the resulting 
    correlation matrix.

    Parameters:
    -----------
    data : pd.DataFrame
        A pandas DataFrame containing the dataset for which the correlation 
        matrix will be computed. The DataFrame should contain numerical values 
        in its columns, as non-numerical data will result in an error.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing the Pearson correlation matrix. The values 
        represent the correlation coefficients, ranging from -1 (perfect negative 
        correlation) to 1 (perfect positive correlation), with 0 indicating no 
        correlation.

    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include='number')
    # Compute and return the Pearson correlation matrix
    matrix_corr = numeric_df.corr(method="pearson")
    print(matrix_corr)
    return matrix_corr

#filename_recipes = "dataset/PP_recipes.csv_extracted/__MACOSX/PP_recipes.csv"
#filename_users = "dataset/PP_users.csv_extracted/__MACOSX/PP_users.csv"
# Uncomment the next line to perform dataset study
# data_recipes = dataset_study(filename_recipes)

#users=dataset_study(filename_users)
#matrix_corr_users=correlation_bio_recipes(users)
#filtering bio recipes
bio_recipes = filtering_bio_recipes_kaggle(r'\b(organic|bio|vegetarian|veggie|homemade|traditional|eco-friendly|local|healthy|farm|seasonal|green|natural|fresh|plant)\b')
#matrix correlation 
matrix_corr=correlation_bio_recipes(bio_recipes)

