from src.utils import df_filtered_bio
import ast
import pandas as pd


def parse_nutrition(nutrition_str):
    """
    Parses a string representation of the nutrition data into a list.

    Args:
        nutrition_str (str): A string containing a list-like format.

    Returns:
        list: A list of nutritional values or a list of None values if parsing fails.
    """
    try:
        # Attempt to parse the string into a Python list using literal_eval
        return ast.literal_eval(nutrition_str)
    except (ValueError, SyntaxError):
        # Return a list of 7 None elements if there's a parsing error
        return [None] * 7


def stats_bio(df_filtered_bio: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate and display various statistical indicators,
    as well as identify the 5 recipes with the highest calorie content.

    Args:
        df_filtered_bio (pd.DataFrame): A filtered DataFrame containing recipes.

    Returns:
        None
    """
    # Apply the parse_nutrition function to the 'nutrition' column
    nutrition_data = df_filtered_bio["nutrition"].dropna().apply(parse_nutrition)
    # Keep only rows where the parsed data has exactly 7 elements
    nutrition_data = nutrition_data[nutrition_data.apply(lambda x: len(x) == 7)]
    # Convert the list of nutrition data into a DataFrame with appropriate column names
    nutrition_df = pd.DataFrame(
        nutrition_data.tolist(),
        columns=[
            "Calories",
            "Total Fat (g)",
            "Sugar (g)",
            "Sodium (mg)",
            "Protein (g)",
            "Saturated Fat (g)",
            "Carbohydrates (g)",
        ],
    )
    # Calculate basic statistical indicators: mean, median, standard deviation, min, max
    combined_df = pd.concat(
        [df_filtered_bio.reset_index(drop=True), nutrition_df], axis=1
    )
    # Add ranking columns for each nutritional component
    combined_df["Calories Rank"] = combined_df["Calories"].rank(
        method="min", ascending=False
    )
    combined_df["Total Fat Rank"] = combined_df["Total Fat (g)"].rank(
        method="min", ascending=False
    )
    combined_df["Sugar Rank"] = combined_df["Sugar (g)"].rank(
        method="min", ascending=False
    )
    combined_df["Sodium Rank"] = combined_df["Sodium (mg)"].rank(
        method="min", ascending=False
    )
    combined_df["Protein Rank"] = combined_df["Protein (g)"].rank(
        method="min", ascending=False
    )
    combined_df["Saturated Fat Rank"] = combined_df["Saturated Fat (g)"].rank(
        method="min", ascending=False
    )
    combined_df["Carbohydrates Rank"] = combined_df["Carbohydrates (g)"].rank(
        method="min", ascending=False
    )
    # Filter to include only the top 5 recipes for each nutritional component
    combined_df["Top 5 Calories"] = combined_df["Calories Rank"] <= 5
    combined_df["Top 5 Total Fat"] = combined_df["Total Fat Rank"] <= 5
    combined_df["Top 5 Sugar"] = combined_df["Sugar Rank"] <= 5
    combined_df["Top 5 Sodium"] = combined_df["Sodium Rank"] <= 5
    combined_df["Top 5 Protein"] = combined_df["Protein Rank"] <= 5
    combined_df["Top 5 Saturated Fat"] = combined_df["Saturated Fat Rank"] <= 5
    combined_df["Top 5 Carbohydrates"] = combined_df["Carbohydrates Rank"] <= 5

    # Displaying the recipes in a dataframe with highest.
    # quantity for each nutritional component
    return combined_df


combined_df = stats_bio(df_filtered_bio)
