import os
import logging
import zipfile
import pandas as pd
import streamlit as st
import ast
from src.metrics import calculate_mtm_score

# Create a logger for this module
logger = logging.getLogger(__name__)


class DataLoader:
    """
    A class for loading, extracting, and processing data files
    for a Streamlit application.
    """

    def __init__(self) -> None:
        """
        Initialize the DataLoader class.
        """
        logger.info("DataLoader initialized.")

    @st.cache_data
    def unzip_data(_self, file_name: str) -> list:
        """
        Extract a ZIP file to a new directory.

        Parameters:
        ----------
        file_name : str
            Path to the ZIP file.

        Returns:
        -------
        list
            List of file paths of the extracted contents.

        Raises:
        ------
        ValueError:
            If the file type is unsupported.
        Exception:
            For any extraction errors.
        """
        try:
            extracted_dir = os.path.splitext(file_name)[0] + "_extracted"

            if not os.path.exists(extracted_dir):
                os.makedirs(extracted_dir)

                if file_name.endswith(".zip"):
                    with zipfile.ZipFile(file_name, "r") as zip_ref:
                        zip_ref.extractall(extracted_dir)
                        logger.info("Extracted ZIP file: %s", file_name)
                else:
                    raise ValueError(f"Unsupported file type for {file_name}")

            return [os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)]

        except Exception as e:
            logger.error("Error while extracting %s: %s", file_name, str(e))
            raise

    @st.cache_data
    def load_data(_self, file_name: str) -> pd.DataFrame:
        """
        Load data from a CSV or ZIP file into a pandas DataFrame.

        Parameters:
        ----------
        file_name : str
            Path to the file.

        Returns:
        -------
        pd.DataFrame
            Loaded data.

        Raises:
        ------
        ValueError:
            If the file type is unsupported.
        Exception:
            For data loading errors.
        """
        try:
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
                logger.info("Loaded CSV file: %s", file_name)

            elif file_name.endswith(".zip"):
                extracted_files = _self.unzip_data(file_name)
                csv_file = next(
                    (f for f in extracted_files if f.endswith(".csv")), None
                )

                if not csv_file:
                    raise ValueError(f"No CSV file found in {file_name}")

                df = pd.read_csv(csv_file)
                logger.info("Loaded CSV from ZIP: %s", csv_file)

            else:
                raise ValueError(f"Unsupported file type: {file_name}")

            return df

        except Exception as e:
            logger.error("Error while loading data from %s: %s", file_name, str(e))
            raise

    @st.cache_data
    def load_and_parse_data(_self, file_name: str) -> tuple:
        """
        Load and parse data, calculating additional metrics and parsing columns.

        Parameters:
        ----------
        file_name : str
            Path to the file.

        Returns:
        -------
        tuple
            A tuple containing:
            - Processed DataFrame.
            - Set of unique ingredients across all rows.

        Raises:
        ------
        Exception:
            For any data loading or processing errors.
        """
        try:
            df = _self.load_data(file_name)

            # Parse "nutrition" column
            df["nutrition"] = df["nutrition"].apply(
                lambda x: (
                    [float(i) for i in ast.literal_eval(x)] if isinstance(x, str) else x
                )
            )

            # Parse "ingredient_PP" column
            df["ingredient_PP"] = df["ingredient_PP"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )

            # Calculate MTM score
            df["mtm_score"] = df["nutrition"].apply(calculate_mtm_score)
            logger.info("Calculated MTM scores for %d recipes.", len(df))

            # Generate unique ingredient list
            ingredient_list = {
                ingredient for sublist in df["ingredient_PP"] for ingredient in sublist
            }
            logger.info(
                "Generated ingredient list with %d unique ingredients.",
                len(ingredient_list),
            )

            return df, ingredient_list

        except Exception as e:
            logger.error(
                "Error while loading and parsing data from %s: %s", file_name, str(e)
            )
            raise
