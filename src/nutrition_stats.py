from utils import df_preprocessed
import ast
import pandas as pd


def parse_nutrition(nutrition_str):
    """
    Parses a string representation of nutritional data into a list of floats.
    The input string typically represents a list-like format.
    with 7 nutritional values,
    and this function extracts those values into a Python list.

    If the input string cannot be parsed correctly.
    (e.g., due to syntax errors or invalid format).
    the function returns a list with seven `None` values.
    which ensures that all returned lists.
    have a consistent length, even in case of parsing failures.

    Args:
        nutrition_str (str): A string that contains a list-like structure.
        with nutritional information.
        The expected format of the string is similar to:
        "[calories, total_fat, sugar, sodium, protein, saturated_fat, carbohydrates]".
        Example: "[250.0, 10.0, 12.0, 200.0, 5.0, 3.0, 30.0]"

    Returns:
        list: A list of 7 nutritional values as floats, or a list of 7 `None` elements
        if the string could not be parsed. The 7 elements correspond to:
            - Calories (float)
            - Total Fat (g) (float)
            - Sugar (g) (float)
            - Sodium (mg) (float)
            - Protein (g) (float)
            - Saturated Fat (g) (float)
            - Carbohydrates (g) (float)

    Example:
        >>> parse_nutrition("[250.0, 10.0, 12.0, 200.0, 5.0, 3.0, 30.0]")
        [250.0, 10.0, 12.0, 200.0, 5.0, 3.0, 30.0]

        >>> parse_nutrition("invalid_string")
        [None, None, None, None, None, None, None]

    Raises:
        None: This function does not raise exceptions but instead catches parsing errors
        and returns a list of `None` values if the input is not in the correct format.
    """
    try:
        # Attempt to parse the string into a Python list using literal_eval
        return ast.literal_eval(nutrition_str)
    except (ValueError, SyntaxError):
        # Return a list of 7 None elements if there's a parsing error
        return [None] * 7


def stats_bio(df_preprocessed: pd.DataFrame) -> pd.DataFrame:
    """
    This function processes a filtered DataFrame of bio recipes and performs.
    the following tasks:
    1. Extracts and parses the 'nutrition' column to convert stringified.
    nutrition data into a usable format.
    2. Calculates statistical indicators (mean, median, etc.) for various.
      nutritional components.
    3. Adds ranking columns to the DataFrame for calories, fats,
        sugars, sodium, proteins.
      saturated fats, and carbohydrates.
    4. Identifies and flags the top 5 recipes in each nutritional component.
    based on the highest values.
    The resulting DataFrame contains the original recipe data.
    the parsed nutritional components.
    the ranking for each component, and boolean flags indicating whether.
    a recipe is in the top 5 for each category.
    Args:
        df_filtered_bio (pd.DataFrame): A filtered DataFrame containing recipe data.
        The DataFrame must include
        a column 'nutrition', where the nutritional information for each recipe.
        is stored as a string.
    Returns
        pd.DataFrame: A DataFrame containing the original recipe data,
        parsed nutritional data, rankings for each nutritional component,
        and boolean flags for top 5 recipes in each category.
    Example:
        # Assuming df_filtered_bio is a DataFrame with a 'nutrition' column.
        # in string format.
        combined_df = stats_bio(df_filtered_bio)
        combined_df.head()  # To see the result
    """
    # Apply the parse_nutrition function to the 'nutrition' column
    nutrition_data = df_preprocessed["nutrition"].dropna().apply(parse_nutrition)
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
        [df_preprocessed.reset_index(drop=True), nutrition_df], axis=1
    )
    # Add ranking columns for each nutritional component
    combined_df["Calories Rank"] = combined_df["Calories"].rank(
        method="min", ascending=True
    )
    combined_df["Total Fat Rank"] = combined_df["Total Fat (g)"].rank(
        method="min", ascending=True
    )
    combined_df["Sugar Rank"] = combined_df["Sugar (g)"].rank(
        method="min", ascending=True
    )
    combined_df["Sodium Rank"] = combined_df["Sodium (mg)"].rank(
        method="min", ascending=True
    )
    combined_df["Protein Rank"] = combined_df["Protein (g)"].rank(
        method="min", ascending=False
    )
    combined_df["Saturated Fat Rank"] = combined_df["Saturated Fat (g)"].rank(
        method="min", ascending=True
    )
    combined_df["Carbohydrates Rank"] = combined_df["Carbohydrates (g)"].rank(
        method="min", ascending=True
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


combined_df = stats_bio(df_preprocessed)
print(combined_df)
