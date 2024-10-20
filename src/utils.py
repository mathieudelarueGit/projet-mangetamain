import pandas as pd
import re  # N'oubliez pas d'importer le module `re` pour les expressions régulières
from src.data_loader import DataLoader

# Loads the raw interactions dataset using the data_loader module
data_loader = DataLoader()
# interactions = data_loader.load_data("dataset/RAW_interactions.csv.zip")
df = data_loader.load_data("dataset/RAW_recipes.csv.zip")


def filter_dataframebis1(
    df: pd.DataFrame, column_names: list, filter_values: list
) -> pd.DataFrame:
    """
    Filters a DataFrame based on specified column names
    and their corresponding filter values.

    Args:
        df (pd.DataFrame): The DataFrame to be filtered.
        column_names (list): A list of column names to filter by.
        filter_values (list): A list of values to filter for each corresponding column.

    Returns:
        pd.DataFrame: A DataFrame containing only the rows
        that match the filter criteria.

    Raises:
        ValueError: If the lengths of column_names and filter_values
        do not match.
        KeyError: If any column in column_names does not exist
        in the DataFrame.
    """
    filtered_df = df.copy()
    for i, column_name in enumerate(column_names):
        if column_name not in filtered_df.columns:
            raise KeyError(f"The column '{column_name}' is not in the DataFrame.")

        value_filter = (
            filter_values[i] if isinstance(filter_values, list) else filter_values
        )

        # Gestion des valeurs None
        if value_filter is None:
            filtered_df = filtered_df[filtered_df[column_name].isnull()]
            continue
        if filtered_df[column_name].dtype == "object":
            if isinstance(value_filter, list):
                filter_pattern_value = "|".join(map(re.escape, value_filter))
                filtered_df = filtered_df[
                    filtered_df[column_name].str.contains(
                        filter_pattern_value, case=False, na=False, regex=True
                    )
                ]
            else:
                filtered_df = filtered_df[
                    filtered_df[column_name].str.contains(
                        value_filter, case=False, na=False, regex=True
                    )
                ]

        elif pd.to_numeric(filtered_df[column_name], errors="coerce").notna().all():
            if isinstance(value_filter, list):
                filtered_df = filtered_df[filtered_df[column_name].isin(value_filter)]
            else:
                filtered_df = filtered_df[filtered_df[column_name] == value_filter]

        elif filtered_df[column_name].dtype.name == "category":
            filtered_df = filtered_df[
                filtered_df[column_name].isin(
                    value_filter if isinstance(value_filter, list) else [value_filter]
                )
            ]
    return filtered_df


# tags bio recipes column
column_names = ["tags"]
# tags bio recipes
filter_values1_bio = [
    [
        "organic",
        "bio",
        "clean",
        "vegetable",
        "vegan",
        "traditional",
        "eco-friendly",
        "local",
        "healthy",
        "seasonal",
        "green",
        "natural",
        "fresh",
        "plant",
        "sustainable",
        "heritage",
        "garden",
        "whole",
        "farm",
    ]
]

df_filtered_bio = filter_dataframebis1(df, column_names, filter_values1_bio)
rate_bio_recipes = float((len(df_filtered_bio) / len(df)) * 100)
