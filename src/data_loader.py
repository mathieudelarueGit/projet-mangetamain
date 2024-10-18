import os
import logging
import zipfile
import lzma
import pandas as pd
import streamlit as st

# Get a logger specific to this module
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        pass

    @st.cache_data
    def decompress_xz(_self, file_name, output_dir):
        """
        Decompresses a plain .xz file into the output directory.
        """
        output_file = os.path.join(
            output_dir, os.path.splitext(os.path.basename(file_name))[0]
        )
        try:
            with lzma.open(file_name, "rb") as xz_file:
                with open(output_file, "wb") as out_file:
                    out_file.write(xz_file.read())
            return output_file
        except Exception as e:
            logger.error(f"Error while decompressing {file_name}: {e}")
            raise

    @st.cache_data
    def unzip_data(_self, file_name: str) -> list:
        """
        Unzips a ZIP or decompresses an XZ file
        and returns a list of the extracted files.
        """
        try:
            extracted_dir = os.path.splitext(file_name)[0] + "_extracted"
            if not os.path.exists(extracted_dir):
                os.makedirs(extracted_dir)

                if file_name.endswith(".zip"):
                    with zipfile.ZipFile(file_name, "r") as zip_ref:
                        zip_ref.extractall(extracted_dir)
                elif file_name.endswith(".xz"):
                    decompressed_file = _self.decompress_xz(file_name, extracted_dir)
                    return [
                        decompressed_file
                    ]  # This should return a list with the decompressed file
                else:
                    raise ValueError(f"Unsupported file type for {file_name}")

            return [os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)]
        except Exception as e:
            logger.error(f"Error while extracting {file_name}: {e}")
            raise

    @st.cache_data
    def load_data(_self, file_name: str) -> pd.DataFrame:
        """
        Loads data from a file (CSV, ZIP containing CSV, or XZ containing CSV).
        """
        logger.info(f"Loading data from {file_name}")  # Log when data is being loaded
        try:
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
                logger.info(f"Loaded CSV file: {file_name}")

            elif file_name.endswith(".zip"):
                extracted_files = _self.unzip_data(file_name)
                csv_file = [f for f in extracted_files if f.endswith(".csv")][0]
                df = pd.read_csv(csv_file)
                logger.info(f"Loaded CSV from ZIP: {csv_file}")

            elif file_name.endswith(".xz"):
                extracted_files = _self.unzip_data(file_name)
                csv_file = extracted_files[0]
                df = pd.read_csv(csv_file)
                logger.info(f"Loaded CSV from XZ: {csv_file}")

            elif file_name.endswith(".pkl"):
                df = pd.read_pickle(file_name)
                logger.info(f"Loaded Pickle file: {file_name}")

            else:
                raise ValueError(f"Unsupported file type: {file_name}")

            return df

        except Exception as e:
            logger.error(f"Error while loading data from {file_name}: {e}")
            raise
