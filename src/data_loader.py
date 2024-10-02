import pandas as pd
import zipfile
import os


def unzip_data(file_name):
    # Extract ZIP file and return the list of extracted files
    extracted_dir = "extracted_files"
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(extracted_dir)

    # Get list of extracted files
    extracted_files = [
        os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir)
    ]
    return extracted_files


def load_data(file_name):
    if file_name.endswith(".csv"):
        # Directly load CSV file
        df = pd.read_csv(file_name)
    elif file_name.endswith(".zip"):
        # Unzip and load the first CSV file found
        extracted_files = unzip_data(file_name)
        csv_file = [f for f in extracted_files if f.endswith(".csv")][
            0
        ]  # Find the first CSV
        df = pd.read_csv(csv_file)
    elif file_name.endswith(".pkl"):
        # Load pickle file
        df = pd.read_pickle(file_name)
    else:
        raise ValueError("Unsupported file type")

    return df
