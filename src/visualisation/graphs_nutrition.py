from nutrition_stats import combined_df
import plotly.express as px
import pandas as pd


def plot_top_4_recipes_by_nutrition(
    combined_df: pd.DataFrame, categories: list
) -> dict:
    """
    Creates a plot for each nutritional category.
    Returns a dictionary with a Plotly figure for each category.
    Args:
        combined_df (pd.DataFrame): DataFrame containing recipe names.
        and their nutritional values.
        categories (list): List of nutritional components to be plotted.
    Returns:
        dict: A dictionary where keys are nutritional categories.
        and values are Plotly figures.
    """
    figures = {}
    for category in categories:
        # Sort recipes depending on the category
        top_4_recipes = combined_df.sort_values(by=category, ascending=False).head(4)

        # Créer un graphique pour la catégorie actuelle
        fig = px.bar(
            top_4_recipes,
            x="name",
            y=category,
            title=f"Top 4 Recipes by {category}",
            labels={"name": "Recipe Name", category: category},
            color_discrete_sequence=["#1f77b4"],
        )

        # Storage the figure in the dictionnary
        figures[category] = fig
    return figures


categories = [
    "Calories",
    "Total Fat (g)",
    "Sugar (g)",
    "Sodium (mg)",
    "Protein (g)",
    "Saturated Fat (g)",
    "Carbohydrates (g)",
]


# Générer les graphiques
nutrition_hist = plot_top_4_recipes_by_nutrition(combined_df, categories)
