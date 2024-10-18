import os
import logging
import zipfile
import lzma

import pandas as pd
import streamlit as st

# Get a logger specific to this module
logger = logging.getLogger(__name__)


@st.cache_data
def decompress_xz(file_name, output_dir):
    """
    Decompresses a plain .xz file into the output directory.
    
    Args:
        file_name (str): Path to the .xz file.
        output_dir (str): Directory where the decompressed file will be stored.
    
    Returns:
        str: Path to the decompressed file.
    """
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file_name))[0])
    with lzma.open(file_name, 'rb') as xz_file:
        with open(output_file, 'wb') as out_file:
            out_file.write(xz_file.read())
    return output_file

@st.cache_data
def unzip_data(file_name: str) -> list:
    """
    Unzips a ZIP or decompresses an XZ file and returns a list of the extracted files. This function
    is cached by Streamlit to prevent repeated unzipping if the file hasn't
    changed.

    Args:
        file_name (str): The path to the ZIP or XZ file to be uncompressed.

    Returns:
        list: A list of paths to the extracted files.

    Raises:
        Exception: If an error occurs during unzipping or uncompressing, logs the error and
                  raises the exception.
    """
    try:
        # Create a unique directory for the extracted files, based on the file name
        extracted_dir = os.path.splitext(file_name)[0] + "_extracted"

        # Check if the directory already exists to avoid unnecessary unzipping
        if not os.path.exists(extracted_dir):
            # Create the directory if it doesn't exist
            os.makedirs(extracted_dir)

            # Handle ZIP files
            if file_name.endswith(".zip"):
                with zipfile.ZipFile(file_name, "r") as zip_ref:
                    zip_ref.extractall(extracted_dir)

            # Handle plain XZ files
            elif file_name.endswith(".xz"):
                decompressed_file = decompress_xz(file_name, extracted_dir)
                logger.info(f"Decompressed XZ file: {decompressed_file}")
                return [decompressed_file]  # Return the decompressed file path as a list

            else:
                raise ValueError(f"Unsupported file type for {file_name}")

        # Create a list of all files in the extracted directory
        extracted_files = [
            os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)
        ]
        logger.info(
            "Successfully extracted %s into %s", file_name, extracted_dir
        )  # Log success
        return extracted_files

    except Exception as e:
        # Log the error and raise the exception
        logger.error(f"Error while extracting {file_name}: {e}")
        raise


@st.cache_data
def load_data(file_name: str) -> pd.DataFrame:
    """
    Loads data from a file (CSV, ZIP containing CSV, or XZ containing CSV). This function
    handles different file types and returns the loaded data as a pandas
    DataFrame. The function is cached to optimize performance.

    Args:
        file_name (str): The path to the file (can be .csv, .zip, or .xz).

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

        # If the file is an XZ (plain .xz), decompress it and load the CSV
        elif file_name.endswith(".xz"):
            extracted_files = unzip_data(file_name)  # Decompress the .xz file
            # We assume the decompressed file is a CSV file
            csv_file = extracted_files[0]  # Get the decompressed file path
            df = pd.read_csv(csv_file)
            logger.info(f"Loaded CSV from XZ: {csv_file}")  # Log success

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
