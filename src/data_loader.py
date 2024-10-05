import os
import logging
import zipfile

import pandas as pd
import streamlit as st
import kaggle
from log_config import *

# Get a logger specific to this module
logger = logging.getLogger(__name__)


@st.cache_data
def unzip_data(file_name: str) -> list:
    """
    Unzips a ZIP file and returns a list of the extracted files. This function is cached
    by Streamlit to prevent repeated unzipping if the ZIP file hasn't changed.

    Args:
        file_name (str): The path to the ZIP file to be unzipped.

    Returns:
        list: A list of paths to the extracted files.

    Raises:
        Exception: If an error occurs during unzipping, logs the error and raises the exception.
    """
    try:
        # Create a unique directory for the extracted files, based on the ZIP file name
        extracted_dir = os.path.splitext(file_name)[0] + "_extracted"

        # Check if the directory already exists to avoid unnecessary unzipping
        if not os.path.exists(extracted_dir):
            os.makedirs(extracted_dir)  # Create the directory if it doesn't exist
            # Extract all files from the ZIP archive into the directory
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(extracted_dir)

        # Create a list of all files in the extracted directory
        extracted_files = [
            os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)
        ]
        logger.info(
            f"Unzipped {file_name} successfully into {extracted_dir}"
        )  # Log success
        return extracted_files

    except Exception as e:
        # Log the error and raise the exception
        logger.error(f"Error while unzipping {file_name}: {e}")
        raise


@st.cache_data
def load_data(file_name: str) -> pd.DataFrame:
    """
    Loads data from a file (CSV, ZIP containing CSV, or Pickle). This function handles
    different file types and returns the loaded data as a pandas DataFrame. The function
    is cached to optimize performance.

    Args:
        file_name (str): The path to the file (can be .csv, .zip, or .pkl).

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        ValueError: If the file type is unsupported.
        Exception: If an error occurs during file loading, logs the error and raises the exception.
    """
    try:
        # If the file is a CSV, load it directly
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_name)
            logger.info(f"Loaded CSV file: {file_name}")  # Log success

        # If the file is a ZIP, unzip it and load the first CSV found
        elif file_name.endswith(".zip"):
            extracted_files = unzip_data(file_name)  # Unzip the file
            # Find the first CSV file in the unzipped files
            csv_file = [f for f in extracted_files if f.endswith(".csv")][0]
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded CSV from ZIP: {csv_file}")  # Log success

        # If the file is a Pickle (.pkl), load it as a DataFrame
        elif file_name.endswith(".pkl"):
            df = pd.read_pickle(file_name)
            logger.info(f"Loaded Pickle file: {file_name}")  # Log success

        # Raise an error if the file type is unsupported
        else:
            raise ValueError(f"Unsupported file type: {file_name}")

        return df

    except Exception as e:
        # Log the error and raise the exception
        logger.error(f"Error while loading data from {file_name}: {e}")
        raise

def load_kaggle_dataset(dataset_slug, filename):
    """
    Loads data from Kaggle.

    Args:
        file_name (str): The path to the file (can be .csv, .zip, or .pkl).
        dataset_slug (str): slug dataset
    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        ValueError: If the file type is unsupported.
        Exception: If an error occurs during file loading, logs the error and raises the exception.
    """
    # Download le dataset
    kaggle.api.dataset_download_files(dataset_slug, path='.', unzip=False)

    # Extract the file
    with zipfile.ZipFile(f'{dataset_slug.split("/")[-1]}.zip', 'r') as z:
        with z.open(filename) as f:
            df = pd.read_csv(f)
    
    # Delete the zip after using
    os.remove(f'{dataset_slug.split("/")[-1]}.zip')
    return df
