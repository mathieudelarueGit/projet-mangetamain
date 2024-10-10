import os
import logging
import zipfile
import requests
import base64
import io
import pandas as pd
import streamlit as st
<<<<<<< HEAD
#import kaggle
from log_config import *
=======
>>>>>>> 5f05405d062bc5f7401a9ec3c501111c5612b306

# Get a logger specific to this module
logger = logging.getLogger(__name__)


@st.cache_data
def unzip_data(file_name: str) -> list:
    """
    Unzips a ZIP file and returns a list of the extracted files. This function
    is cached by Streamlit to prevent repeated unzipping if the ZIP file hasn't
    changed.

    Args:
        file_name (str): The path to the ZIP file to be unzipped.

    Returns:
        list: A list of paths to the extracted files.

    Raises:
        Exception: If an error occurs during unzipping, logs the error and
                  raises the exception.
    """
    try:
        # Create a unique directory for the extracted files, based on the ZIP
        # file name
        extracted_dir = os.path.splitext(file_name)[0] + "_extracted"

        # Check if the directory already exists to avoid unnecessary unzipping
        if not os.path.exists(extracted_dir):
            # Create the directory if it doesn't exist
            os.makedirs(extracted_dir)
            # Extract all files from the ZIP archive into the directory
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(extracted_dir)

        # Create a list of all files in the extracted directory
        extracted_files = [
            os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)
        ]
        logger.info(
            "Unzipped %s successfully into %s", file_name, extracted_dir
        )  # Log success
        return extracted_files

    except Exception as e:
        # Log the error and raise the exception
        logger.error(f"Error while unzipping {file_name}: {e}")
        raise


@st.cache_data
def load_data(file_name: str) -> pd.DataFrame:
    """
    Loads data from a file (CSV, ZIP containing CSV, or Pickle). This function
    handles different file types and returns the loaded data as a pandas
    DataFrame. The function is cached to optimize performance.

    Args:
        file_name (str): The path to the file (can be .csv, .zip, or .pkl).

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        ValueError: If the file type is unsupported.
        Exception: If an error occurs during file loading, logs the error and
                  raises the exception.
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

def load_data_kaggle(base_url: str, owner_slug: str, dataset_slug: str, dataset_version: str, file_name: str) -> pd.DataFrame:
    """
    Downloads a dataset from Kaggle and loads it into a pandas DataFrame.

    Args:
        base_url (str): The base URL for the Kaggle API.
        owner_slug (str): The owner of the dataset (username).
        dataset_slug (str): The name of the dataset.
        dataset_version (str): The version number of the dataset.

    Returns:
        pd.DataFrame: A DataFrame containing the dataset loaded from the downloaded CSV file.

    Raises:
        ValueError: If the DataFrame is empty or not loaded correctly.
    """
    try:
        # Construct the URL for the dataset download
        url = f"{base_url}/datasets/download/{owner_slug}/{dataset_slug}?datasetVersionNumber={dataset_version}"

        # Encode the username and key for basic authentication with taping in the console
        username_ = input("What's your username ? ")
        key_api = input("What's your key ? ")
        creds = base64.b64encode(bytes(f"{username_}:{key_api}", "ISO-8859-1")).decode("ascii")
        
        headers = {
            "Authorization": f"Basic {creds}"
        }

        # Send a GET request to the URL with the authorization headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error downloading the dataset. Status: {response.status_code}")
            logger.error(f"Error downloading the dataset. Status: {response.status_code}")
            print("Response content:", response.text[:1000])  # Display the first 1000 characters of the response content
            return None  # Return None if the request fails

        # Check if the content type of the response is a ZIP file
        content_type = response.headers.get('Content-Type')
        if content_type == 'application/zip':
            try:
                # Load the response content as a ZIP file
                zf = zipfile.ZipFile(io.BytesIO(response.content))

                # Specify the expected CSV file name within the ZIP archive
                #file_name = "RAW_recipes.csv"  # Replace with the actual name of the CSV file in the ZIP
                with zf.open(file_name) as file:
                    df = pd.read_csv(file)
                    logger.info(f"Loaded CSV file: {file_name}")
                    # Check if the DataFrame is loaded correctly and is not empty
                    if df is None or df.empty:
                        logger.error(f"The DataFrame in file {file_name} was not loaded correctly or is empty")
                        raise ValueError("The DataFrame was not loaded correctly or is empty.")
                        
                    # Optionally, print the first few rows of the DataFrame for confirmation
                    print(df.head())
                    return df  # Return the loaded DataFrame

            except zipfile.BadZipFile:
                
                logger.error(f"Error: The downloaded file is not a valid ZIP file.: {file_name}")
        else:
            print(f"Error: The downloaded file is not a ZIP file. Content-Type: {content_type}")
            print(response.content[:1000])  # Display a portion of the content for diagnostic purposes
            return None  # Return None if the content is not a ZIP file
    
    except Exception as e:
        # Log the error and raise the exception
        logger.error(f"Error while loading data from {file_name}: {e}")
        raise
    