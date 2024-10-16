import os
print("Répertoire de travail graphs :", os.getcwd())

import pandas as pd
import plotly.express as px

from data_loader import *


# Loads the raw interactions dataset using data_loader
interactions = load_data("dataset/RAW_interactions.csv_extracted/RAW_interactions.csv")
# interactions = load_data("dataset/PP_recipes.csv.zip")

# Creates a DataFrame with the count of each rating
ratio_of_ratings = pd.DataFrame(interactions.rating.value_counts())
ratio_of_ratings.columns = ['count'] # Renaming the column to 'count'
# top10_hottest_recipes = interactions.recipe_id.value_counts().head(10)
top10_hottest_recipes = "Best Banana Bread\nTo Die For Crock Pot Roast\nCrock Pot Chicken with Black Beans and Cream Cheese\nCreamy Cajun Chicken Pasta\nBest Ever Banana Cake with Cream Cheese Frosting\nYes, Virginia, There is a Great Meatloaf\nJo Mama's World Famous Spaghetti\nWhatever Floats Your Boat Brownies\nKittencal's Italian Melt in Your Mouth Meatballs\nJapanese Mum's Chicken"

# Ajouter une colonne 'ratio' qui contiendra les ratios de chaque note
ratio_of_ratings['ratio'] = ratio_of_ratings['count'] / ratio_of_ratings['count'].sum()

# Creation of the pie chart representing the distribution of ratings
fig1 = px.pie(
    ratio_of_ratings, 
    names=ratio_of_ratings.index,  # Utilise les index (les notes) comme labels
    values='count',  # Utilise la colonne 'count' pour la taille des sections
    title='Ratio of ratings in the dataset',
    color=ratio_of_ratings.index,  # Utilise les index pour définir la couleur
    color_discrete_sequence=px.colors.sequential.Blues[::-1]  # Nuances du rouge clair au rouge foncé
)

# Updates the layout of the pie chart to display the percentage and the label
fig1.update_traces(textinfo='label+percent')


fig2 = px.histogram(
    interactions.date,
    title='Dynamics in time'
)

fig2.add_annotation(
    text="Instagramm",
    x='2011-10-31',  # Position x dans l'intervalle (ajustez si nécessaire)
    y=6000,  # Position y (80% de la hauteur de la courbe)
    # xref=f'x{(i + 1)}',  # Référence à l'axe x de la sous-figure
    # yref=f'y{(i + 1)}',  # Référence à l'axe y de la sous-figure
    showarrow=False,
    font=dict(size=15, color="black"),
    bgcolor="rgba(255, 255, 255, 0.7)",  # Fond blanc semi-transparent
    bordercolor="black",
    borderwidth=1,
    borderpad=4
)

# Mettre à jour les labels des axes
fig2.update_layout(
    xaxis_title="Time",  # Label pour l'axe x
    yaxis_title="Amount of interactions"  # Label pour l'axe y
)

fig3 = px.scatter(interactions.recipe_id.value_counts(),
                title='Too popular to be serious')


fig3.add_annotation(
    text="Buzzing zone",
    x=197730,  # Position x dans l'intervalle (ajustez si nécessaire)
    y=1000,  # Position y (80% de la hauteur de la courbe)
    showarrow=False,
    font=dict(size=15, color="black"),
    bgcolor="rgba(255, 255, 255, 0.7)",  # Fond blanc semi-transparent
    bordercolor="black",
    borderwidth=1,
    borderpad=4
)

fig3.update_layout(
    # xaxis_title="All the recipes stored in the data",  # Label pour l'axe x
    yaxis_title="Nb of interactions for each recipe",  # Label pour l'axe y
    showlegend=False,  # Cacher la légende
    xaxis=dict(
        tickvals=[],  # Pas de valeurs affichées sur l'axe des x
        showline=False  # Ne pas afficher la ligne de l'axe   
    )
)

# Ajouter un rectangle transparent pour surligner la zone supérieure à 500
fig3.add_shape(
    type="rect",
    x0=fig3.data[0].x.min(),  # Position de départ en x (min de l'axe des x)
    x1=fig3.data[0].x.max(),  # Position de fin en x (max de l'axe des x)
    y0=500,  # Position de départ en y (500)
    y1=fig3.data[0].y.max(),  # Position de fin en y (max de l'axe des y)
    line=dict(color="rgba(255, 0, 0, 0)"),  # Pas de bordure visible
    fillcolor="rgba(255, 0, 0, 0.2)"  # Rouge transparent
)

# class Functions:

#     # constructeur
#     def __init__(self) -> None:
#         pass

#     @staticmethod
#     # renvoyer les 5 premières lignes du
#     def head_dataframe(path_to_dataframe: str) -> str:
#         """_summary_
#         This method is called to display the first 5 lines of any Dataframe.
#         The dataframe is refered to its relative path as the sole argument.
#         Returns:
#             str: equivalent to df.head()
#         """

#         try:
#             df = pd.read_csv(path_to_dataframe)
#         except Exception as e:
#             # TODO: log the error in the notebook
#             logging.error(
#                 f"Erreur lors de la lecture du fichier CSV spécifié à  \ l'emplacement {path_to_dataframe}: {e}"
#             )
#             print(e)

#         to_display = df.head().to_string()
#         return to_display
