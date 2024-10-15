import logging
import pandas as pd
import numpy as np
import streamlit as st
import re
from log_config import *
from data_loader import *
import matplotlib.pyplot as plt
import re
import ast
from log_config import *
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from data_loader import *
# Get a logger specific to this module
logger = logging.getLogger(__name__)

df = load_data("dataset/RAW_recipes.csv.zip")
print(df)

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
    # Print column names
    print("Column names:", df.columns)
    # Print data description
    print(df.describe())
    # Analyze missing data
    print("Number of missing data:", df.isnull().sum().sum())
    return df


def filtering_dataframe(df: pd.DataFrame, key_words_bio: str) -> pd.DataFrame:
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
    #base_url = "https://www.kaggle.com/api/v1"
    #owner_slug = "shuyangli94"
    #dataset_slug = "food-com-recipes-and-user-interactions"
    #dataset_version = "2"
    #file_name="RAW_recipes.csv"
    #df_raw_recipes = load_data_kaggle(base_url, owner_slug, dataset_slug, dataset_version, file_name)
    #key_words_bio = r'\b(organic|bio|clean|vegetable|vegan|traditional|eco-friendly|local|healthy|seasonal|green|natural|fresh|plant|sustainable|heritage|garden|whole|farm)\b'
    # Filtering recipes with the tags bio, organic, traditional, gluten-free, veggie
    #bio_recipes1 = df[df['tags'].str.contains(key_words_bio, case=False, na=False, regex=True)]
    #print(bio_recipes1)
    #return bio_recipes1
    #return bio_recipes1

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
#bio_recipes = filtering_bio_recipes_kaggle(r'\b(organic|bio|clean|vegetable|vegan|traditional|eco-friendly|local|healthy|seasonal|green|natural|fresh|plant|sustainable|heritage|garden|whole|farm)\b')
#69173 recipes found with the list of keywords
#matrix correlation 
#matrix_corr=correlation_bio_recipes(bio_recipes)

def filter_dataframebis1(df: pd.DataFrame, column_names: list, filter_values: list) -> pd.DataFrame:
    """
    Filters a DataFrame based on specified column names and their corresponding filter values.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.
        column_names (list): A list of column names to filter by.
        filter_values (list): A list of values to filter for each corresponding column.
        
    Returns:
        pd.DataFrame: A DataFrame containing only the rows that match the filter criteria.

    Raises:
        ValueError: If the lengths of column_names and filter_values do not match.
        KeyError: If any column in column_names does not exist in the DataFrame.
    """
    # Calling the dataset_study function to analyze the DataFrame (ensure this function is defined elsewhere)
    #df = dataset_study(df)
    filtered_df = df.copy()

    # If filtering by only one column in the dataset
    if isinstance(filter_values, list) and len(column_names) != len(filter_values):
        raise ValueError("The lengths of column_names and filter_values are different. They must match.")

    for i, column_name in enumerate(column_names):
        # Check if the column name is in the DataFrame's columns
        if column_name not in filtered_df.columns:
            raise KeyError(f"The column '{column_name}' is not in the DataFrame.")

        # Use the corresponding value from filter_values or a default value if not provided
        value_filter = filter_values[i] if isinstance(filter_values, list) else filter_values

        # Case 1: string columns (dtype is object)
        if filtered_df[column_name].dtype == 'object':
            # Use str.contains for regex
            if isinstance(value_filter, list):
                # Create a regex pattern from the list of filter values
                filter_pattern_value = '|'.join(map(re.escape, value_filter))
                filtered_df = filtered_df[filtered_df[column_name].str.contains(filter_pattern_value, case=False, na=False, regex=True)]
            else:
                filtered_df = filtered_df[filtered_df[column_name].str.contains(value_filter, case=False, na=False, regex=True)]

        # Case 2: numeric columns
        elif pd.to_numeric(filtered_df[column_name], errors='coerce').notna().all():
            if isinstance(value_filter, list):
                filtered_df = filtered_df[filtered_df[column_name].isin(value_filter)]
            else:
                filtered_df = filtered_df[filtered_df[column_name] == value_filter]

        # Case 3: other types of columns such as categorical, datetime.
        elif filtered_df[column_name].dtype.name == 'category':
            filtered_df = filtered_df[filtered_df[column_name].isin(value_filter if isinstance(value_filter, list) else [value_filter])]
    return filtered_df

#df_filtered_bio=filtering_dataframe(df,r'\b(organic|bio|clean|vegetable|vegan|traditional|eco-friendly|local|healthy|seasonal|green|natural|fresh|plant|sustainable|heritage|garden|whole|farm)\b')
#print(df_filtered_bio)
#column_names=['id']
column_names=['tags','n_ingredients']
#column_names=['n_ingredients']
#column_names=['n_ingredients','contributor_id']
#column_names=['tags']
#column_names=['tags', 'contributor_id']
#column_names=['tags', 'minutes']
#column_names=['tags']
#column_names=['minutes']
#filter_values1=r'\b(30/60)\b'
#filter_values1=[[30,60]]
#filter_values1=[['organic', 'bio', 'clean', 'vegetable', 'vegan', 'traditional', 'eco-friendly', 'local', 'healthy', 'seasonal', 'green', 'natural', 'fresh', 'plant', 'sustainable', 'heritage', 'garden', 'whole', 'farm'],[60,90,130]]
#filter_values1=[['organic', 'bio', 'clean', 'vegetable', 'vegan', 'traditional', 'eco-friendly', 'local', 'healthy', 'seasonal', 'green', 'natural', 'fresh', 'plant', 'sustainable', 'heritage', 'garden', 'whole', 'farm'],[2.002290e+09,5.534885e+06]]
#filter_values1=[['organic', 'bio', 'clean', 'vegetable', 'vegan', 'traditional', 'eco-friendly', 'local', 'healthy', 'seasonal', 'green', 'natural', 'fresh', 'plant', 'sustainable', 'heritage', 'garden', 'whole', 'farm']]
#filter_values1=r'\b(organic|bio|clean|vegetable|vegan|traditional|eco-friendly|local|healthy|seasonal|green|natural|fresh|plant|sustainable|heritage|garden|whole|farm)\b'
#filter_values1=[
#    ['organic', 'bio', 'clean', 'vegetable', 'vegan', 'traditional', 'eco-friendly', 'local', 'healthy', 'seasonal', 'green', 'natural', 'fresh', 'plant', 'sustainable', 'heritage', 'garden', 'whole', 'farm'],  # Filtre pour les tags
#    [30, 60,90,130]  # minutes filter values
#]
filter_values1=[
    ['organic', 'bio', 'clean', 'vegetable', 'vegan', 'traditional', 'eco-friendly', 'local', 'healthy', 'seasonal', 'green', 'natural', 'fresh', 'plant', 'sustainable', 'heritage', 'garden', 'whole', 'farm'],  # Filtre pour les tags
    [9,11,13,18]  # contributor_id filter values
]
#filter_values1=[
      # Filtre pour les tags
#    [9,11,13,18], 
#    [2.002290e+09] # contributor_id filter values
#]
#caution strings
#filter_values1=[[30,60]]
#filter_values1=[[9,11,13,18]]
#filter_values1=r'\b(organic|bio|clean|vegetable|vegan|traditional|eco-friendly|local|healthy|seasonal|green|natural|fresh|plant|sustainable|heritage|garden|whole|farm)\b'
df_filtered_bio=filter_dataframebis1(df,column_names,filter_values1)
print(f"Number of rows in the filtered dataset: {len(df_filtered_bio)}")

def parse_nutrition(nutrition_str: str)->float:
    """Convert an string to a float."""
    return np.array(ast.literal_eval(nutrition_str))

def cluster_nutrition_data(df_filtered_bio, eps, min_samples):
    # Parse the nutrition column
    nutrition_data = df_filtered_bio['nutrition'].dropna().apply(parse_nutrition)
    
    # Convert to DataFrame
    nutrition_df = pd.DataFrame(nutrition_data.tolist(), columns=[
        'Calories', 'Total Fat (g)', 'Sugar (g)', 'Sodium (mg)', 'Protein (g)', 
        'Saturated Fat (g)', 'Carbohydrates (g)'
    ])

    # Standardize the data
    scaler = StandardScaler()
    nutrition_data_scaled = scaler.fit_transform(nutrition_df)

    # Apply DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(nutrition_data_scaled)

    # Add clusters to data
    nutrition_df['cluster'] = clusters

    # Visualization function
    def plot_clusters(x, y, xlabel, ylabel, title, filename):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=nutrition_df[x], y=nutrition_df[y], hue=clusters, palette='viridis', legend='full')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(filename)
        plt.show()
    
    # Plot clusters
    plot_clusters('Calories', 'Total Fat (g)', 'Calories', 'Total Fat', 'Clustering by Calories and Total Fat', 'src/models/cluster_fat_calories1.png')
    plot_clusters('Saturated Fat (g)', 'Sodium (mg)', 'Saturated Fat', 'Sodium', 'Clustering by Saturated Fat and Sodium', 'src/models/cluster_sodium_saturated_fat1.png')
    plot_clusters('Sugar (g)', 'Saturated Fat (g)', 'Sugar', 'Saturated Fat', 'Clustering by Sugar and Saturated Fat', 'src/models/cluster_saturatedfat_sugar1.png')
    plot_clusters('Sodium (mg)', 'Protein (g)', 'Sodium', 'Protein', 'Clustering by Sodium and Protein', 'src/models/cluster_sodium_proteins1.png')
    plot_clusters('Total Fat (g)', 'Carbohydrates (g)', 'Total Fat', 'Carbohydrates', 'Clustering by Total Fat and Carbohydrates', 'src/models/cluster_fat_carbohydrates1.png')
    plot_clusters('Calories', 'Carbohydrates (g)', 'Calories', 'Carbohydrates', 'Clustering by Calories and Carbohydrates', 'src/models/cluster_calories_carbohydrates.png')
    

eps=1.2
min_samples=8
# Usage example
cluster_nutrition_data(df_filtered_bio,eps,min_samples)