import os
import logging
import zipfile
import pandas as pd
import streamlit as st
import ast

from metrics import calculate_mtm_score

# Get a logger specific to this module
logger = logging.getLogger(__name__)


class DataLoader:
    """
    A class for loading, extracting, and processing data files
    for a Streamlit application.
    """

    def __init__(self):
        """
        Initializes the DataLoader class.
        """
        pass

    @st.cache_data
    def unzip_data(_self, file_name: str) -> list:
        """
        Unzips a ZIP file and extracts its contents to a new directory.

        Parameters:
        ----------
        file_name : str
            The path to the ZIP file to be extracted.

        Returns:
        -------
        list
            A list of file paths of the extracted contents.

        Raises:
        ------
        ValueError:
            If the file type is not supported.
        Exception:
            If an error occurs during extraction.
        """
        try:
            extracted_dir = os.path.splitext(file_name)[0] + "_extracted"
            if not os.path.exists(extracted_dir):
                os.makedirs(extracted_dir)

                if file_name.endswith(".zip"):
                    with zipfile.ZipFile(file_name, "r") as zip_ref:
                        zip_ref.extractall(extracted_dir)
                else:
                    raise ValueError(f"Unsupported file type for {file_name}")

            return [os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)]
        except Exception as e:
            logger.error(f"Error while extracting {file_name}: {e}")
            raise

    @st.cache_data
    def load_data(_self, file_name: str) -> pd.DataFrame:
        """
        Loads data from a CSV or ZIP file into a pandas DataFrame.

        Parameters:
        ----------
        file_name : str
            The path to the file to be loaded.

        Returns:
        -------
        pd.DataFrame
            The loaded data as a pandas DataFrame.

        Raises:
        ------
        ValueError:
            If the file type is not supported.
        Exception:
            If an error occurs during data loading.
        """
        logger.info(f"Loading data from {file_name}")
        try:
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
                logger.info(f"Loaded CSV file: {file_name}")

            elif file_name.endswith(".zip"):
                extracted_files = _self.unzip_data(file_name)
                csv_file = [f for f in extracted_files if f.endswith(".csv")][0]
                df = pd.read_csv(csv_file)
                logger.info(f"Loaded CSV from ZIP: {csv_file}")
            else:
                raise ValueError(f"Unsupported file type: {file_name}")

            return df

        except Exception as e:
            logger.error(f"Error while loading data from {file_name}: {e}")
            raise

    @st.cache_data
    def load_and_parse_data(_self, file_name: str):
        """
        Loads and processes a data file, parsing specific columns
        and calculating additional metrics.

        Parameters:
        ----------
        file_name : str
            The path to the data file to be loaded and processed.

        Returns:
        -------
        tuple
            A tuple containing:
            - A pandas DataFrame with processed data.
            - A set of unique ingredients across all rows.

        Raises:
        ------
        Exception:
            If an error occurs during data loading or processing.
        """
        try:
            # Load data
            df = _self.load_data(file_name)

            # Parse nutrition and ingredient_PP columns
            df["nutrition"] = df["nutrition"].apply(
                lambda x: (
                    [float(i) for i in ast.literal_eval(x)] if isinstance(x, str) else x
                )
            )
            df["ingredient_PP"] = df["ingredient_PP"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )

            # Calculate and add the MTM score column
            df["mtm_score"] = df["nutrition"].apply(calculate_mtm_score)

            # Generate sorted ingredient list
            ingredient_list = set(
                ingredient for sublist in df["ingredient_PP"] for ingredient in sublist
            )

            return df, ingredient_list

        except Exception as e:
            logger.error(f"Error while loading and parsing data from {file_name}: {e}")
            raise
