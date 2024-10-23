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
    mean_nutrition = nutrition_df.mean()  # Moyenne
    median_nutrition = nutrition_df.median()  # Médiane
    std_nutrition = nutrition_df.std()  # Écart-type
    min_nutrition = nutrition_df.min()  # Minimum
    max_nutrition = nutrition_df.max()  # Maximum
    print("Mean : \n", mean_nutrition)
    print("Median : \n", median_nutrition)
    print("Standard  : \n", std_nutrition)
    print("Minimums : \n", min_nutrition)
    print("Maximums : \n", max_nutrition)
    combined_df = pd.concat(
        [df_filtered_bio.reset_index(drop=True), nutrition_df], axis=1
    )
    # Sort the combined DataFrame and select the top 5 for each nutritional component
    high_calories_recipes = combined_df.sort_values(
        by="Calories", ascending=False
    ).head(5)[["name", "nutrition", "Calories"]]
    high_Total_Fat_recipes = combined_df.sort_values(
        by="Total Fat (g)", ascending=False
    ).head(5)[["name", "nutrition", "Total Fat (g)"]]
    high_sugar_recipes = combined_df.sort_values(by="Sugar (g)", ascending=False).head(
        5
    )[["name", "nutrition", "Sugar (g)"]]
    high_sodium_recipes = combined_df.sort_values(
        by="Sodium (mg)", ascending=False
    ).head(5)[["name", "nutrition", "Sodium (mg)"]]
    high_proteins_recipes = combined_df.sort_values(
        by="Protein (g)", ascending=False
    ).head(5)[["name", "nutrition", "Protein (g)"]]
    high_satured_recipes = combined_df.sort_values(
        by="Saturated Fat (g)", ascending=False
    ).head(5)[["name", "nutrition", "Saturated Fat (g)"]]
    high_carbohydrates_recipes = combined_df.sort_values(
        by="Carbohydrates (g)", ascending=False
    ).head(5)[["name", "nutrition", "Carbohydrates (g)"]]

    # Displaying the recipes in a dataframe with highest.
    # quantity for each nutritional component
    print("Recipes with highest quantity of calories :")
    print(high_calories_recipes)
    print("Recipes with highest quantity of total fat:")
    print(high_Total_Fat_recipes)
    print("Recipes with highest quantity of sugar:")
    print(high_sugar_recipes)
    print("Recipes with highest quantity of sodium:")
    print(high_sodium_recipes)
    print("Recipes with highest quantity of proteins:")
    print(high_proteins_recipes)
    print("Recipes with highest quantity of satured fat:")
    print(high_satured_recipes)
    print("Recipes with highest quantity of carbohydrates:")
    print(high_carbohydrates_recipes)
    """
    # the number of ingredients vs nutritional composition
    if "ingredients" in df_filtered_bio.columns:
        # Number of ingredients
        combined_df["n_ingredients"] = df_filtered_bio["ingredients"].apply(
            lambda x: len(ast.literal_eval(x)) if isinstance(x, str) else 0
        )

        # Correlation between number of ingredients and calories
        correlation_calories = combined_df["n_ingredients"].corr(
            combined_df["Calories"]
        )
        print(
            f"\nCorrelation number of ingredients vs calories:{correlation_calories:2f}"
        )

        # Checking if recipes with more ingredients are higher in calories
        high_calorie_mean = combined_df[
            combined_df["Calories"] > combined_df["Calories"].median()
        ]["n_ingredients"].mean()
        low_calorie_mean = combined_df[
            combined_df["Calories"] <= combined_df["Calories"].median()
        ]["n_ingredients"].mean()

        print(
            f"(Avg)number ingredients in high-calorierecipes: {high_calorie_mean:.2f}"
        )
        print(f"(Avg)number ingredients in low-calorie recipes: {low_calorie_mean:.2f}")
    else:
        print("\n'ingredients' column not found in the DataFrame.")
    if "ingredients" in df_filtered_bio.columns:
        # Number of ingredients
        combined_df["n_ingredients"] = df_filtered_bio["ingredients"].apply(
            lambda x: len(ast.literal_eval(x)) if isinstance(x, str) else 0
        )

        # Correlation between number of ingredients and proteins
        correlation_proteins = combined_df["n_ingredients"].corr(
            combined_df["Protein (g)"]
        )
        print(f"\nCorr number of ingredients vs proteins: {correlation_proteins:.2f}")

        # Checking if recipes with more ingredients are higher in calories
        high_proteins_mean = combined_df[
            combined_df["Protein (g)"] > combined_df["Protein (g)"].median()
        ]["n_ingredients"].mean()
        low_proteins_mean = combined_df[
            combined_df["Protein (g)"] <= combined_df["Protein (g)"].median()
        ]["n_ingredients"].mean()

        print(
            f"(Avg)numberingredients in high-proteinsrecipes: {high_proteins_mean:.2f}"
        )
        print(
            f"(Avg)number ingredients in low-proteinsrecipes: {low_proteins_mean:.2f}"
        )
    else:
        print("\n'ingredients' column not found in the DataFrame.")
    if "ingredients" in df_filtered_bio.columns:
        # Number of ingredients
        combined_df["n_ingredients"] = df_filtered_bio["ingredients"].apply(
            lambda x: len(ast.literal_eval(x)) if isinstance(x, str) else 0
        )

        # Correlation between number of ingredients and proteins
        correlation_sugar = combined_df["n_ingredients"].corr(combined_df["Sugar (g)"])
        print(f"\nCorr number of ingredients vs sugar: {correlation_sugar:.2f}")

        # Checking if recipes with more ingredients are higher in calories
        high_sugar_mean = combined_df[
            combined_df["Sugar (g)"] > combined_df["Sugar (g)"].median()
        ]["n_ingredients"].mean()
        low_sugar_mean = combined_df[
            combined_df["Sugar (g)"] <= combined_df["Sugar (g)"].median()
        ]["n_ingredients"].mean()

        print(f"(Avg)number ingredients in high-sugar recipes: {high_sugar_mean:.2f}")
        print(f"(Avg)number ingredients in low-sugar recipes: {low_sugar_mean:.2f}")
    else:
        print("\n'ingredients' column not found in the DataFrame.")
    if "ingredients" in df_filtered_bio.columns:
        # Number of ingredients
        combined_df["n_ingredients"] = df_filtered_bio["ingredients"].apply(
            lambda x: len(ast.literal_eval(x)) if isinstance(x, str) else 0
        )

        # Correlation between number of ingredients and proteins
        correlation_sodium = combined_df["n_ingredients"].corr(
            combined_df["Sodium (mg)"]
        )
        print(f"\nCorr number of ingredientsvssodium : {correlation_sodium:.2f}")

        # Checking if recipes with more ingredients are higher in calories
        high_sodium_mean = combined_df[
            combined_df["Sodium (mg)"] > combined_df["Sodium (mg)"].median()
        ]["n_ingredients"].mean()
        low_sodium_mean = combined_df[
            combined_df["Sodium (mg)"] <= combined_df["Sodium (mg)"].median()
        ]["n_ingredients"].mean()

        print(f"(Avg)number ingredients in high-sodium rec: {high_sodium_mean:.2f}")
        print(f"(Avg)number ingredients in low-sodium rec: {low_sodium_mean:.2f}")
    else:
        print("\n'ingredients' column not found in the DataFrame.")
    if "ingredients" in df_filtered_bio.columns:
        # Number of ingredients
        combined_df["n_ingredients"] = df_filtered_bio["ingredients"].apply(
            lambda x: len(ast.literal_eval(x)) if isinstance(x, str) else 0
        )

        # Correlation between number of ingredients and proteins
        correlation_carbohydrates = combined_df["n_ingredients"].corr(
            combined_df["Carbohydrates (g)"]
        )
        print(f"\nCorr ingredients vs carbohydrates: {correlation_carbohydrates:.2f}")

        # Checking if recipes with more ingredients are higher in calories
        high_carbohydrates_mean = combined_df[
            combined_df["Carbohydrates (g)"] > combined_df["Carbohydrates (g)"].median()
        ]["n_ingredients"].mean()
        low_carbohydrates_mean = combined_df[
            combined_df["Carbohydrates (g)"] < combined_df["Carbohydrates (g)"].median()
        ]["n_ingredients"].mean()

        print(
            f"Avgnumberingredients in high-carbohydrates: {high_carbohydrates_mean:.2f}"
        )
        print(
            f"(Avg)numberingredients in low-carbohydrates: {low_carbohydrates_mean:.2f}"
        )
    else:
        print("\n'ingredients' column not found in the DataFrame.")
    """
    return combined_df


combined_df = stats_bio(df_filtered_bio)
