import pytest
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import DataLoader
import plotly.express as px
from src.visualisation import graphs


@pytest.fixture
def interactions_data():
    # Simule le chargement des données en utilisant le DataLoader
    data_loader = DataLoader()
    interactions = data_loader.load_data("dataset/RAW_interactions.csv.xz")
    return interactions


def test_interactions_loading(interactions_data):
    # Vérifie que les données sont bien chargées sous forme de DataFrame
    assert isinstance(
        interactions_data, pd.DataFrame
    ), "Les données ne sont pas un DataFrame."
    # Vérifie que certaines colonnes critiques existent
    assert "rating" in interactions_data.columns, "La colonne 'rating' est manquante."
    assert "date" in interactions_data.columns, "La colonne 'date' est manquante."
    assert (
        "recipe_id" in interactions_data.columns
    ), "La colonne 'recipe_id' est manquante."


def test_ratio_of_ratings(interactions_data):
    # Calcule le ratio des ratings
    ratio_of_ratings = pd.DataFrame(interactions_data.rating.value_counts())
    ratio_of_ratings.columns = ["count"]
    ratio_of_ratings["ratio"] = (
        ratio_of_ratings["count"] / ratio_of_ratings["count"].sum()
    )

    # Vérifie que le DataFrame contient bien les colonnes 'count' et 'ratio'
    assert "count" in ratio_of_ratings.columns, "La colonne 'count' est manquante."
    assert "ratio" in ratio_of_ratings.columns, "La colonne 'ratio' est manquante."
    assert (
        ratio_of_ratings["count"].sum() == interactions_data.shape[0]
    ), "La somme des 'count' ne correspond pas au nombre total d'interactions."


def test_pie_chart_creation(interactions_data):
    # Crée un DataFrame avec les ratios
    ratio_of_ratings = pd.DataFrame(interactions_data.rating.value_counts())
    ratio_of_ratings.columns = ["count"]
    ratio_of_ratings["ratio"] = (
        ratio_of_ratings["count"] / ratio_of_ratings["count"].sum()
    )

    # Crée le pie chart
    fig1 = px.pie(
        ratio_of_ratings,
        names=ratio_of_ratings.index,
        values="count",
        title="Ratio of ratings in the dataset",
        color=ratio_of_ratings.index,
        color_discrete_sequence=px.colors.sequential.Blues[::-1],
    )

    # Vérifie que le graphique est bien un objet de type Figure
    assert isinstance(
        fig1, go.Figure
    ), "Le graphique n'est pas un objet de type Figure."


def test_histogram_creation(interactions_data):
    # Crée un histogramme
    fig2 = px.histogram(interactions_data.date, title="Dynamics in time")

    # Vérifie que le graphique est bien un objet de type Figure
    assert isinstance(
        fig2, go.Figure
    ), "Le graphique n'est pas un objet de type Figure."

    # Vérifie que le titre est correct
    assert (
        fig2.layout.title.text == "Dynamics in time"
    ), "Le titre de l'histogramme n'est pas correct."


def test_scatter_plot_creation(interactions_data):
    # Crée un scatter plot
    fig3 = px.scatter(
        interactions_data.recipe_id.value_counts(), title="Too popular to be serious"
    )

    # Vérifie que le graphique est bien un objet de type Figure
    assert isinstance(
        fig3, go.Figure
    ), "Le graphique n'est pas un objet de type Figure."

    # Vérifie que le titre est correct
    assert (
        fig3.layout.title.text == "Too popular to be serious"
    ), "Le titre du scatter plot n'est pas correct."


def test_annotations_in_figures(interactions_data):
    # Crée un histogramme
    fig2 = px.histogram(interactions_data.date, title="Dynamics in time")
    fig2.add_annotation(
        text="Instagram",
        x="2012-01-31",
        y=6000,
        showarrow=False,
        font=dict(size=15, color="black"),
        bgcolor="rgba(255, 255, 255, 0.7)",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
    )

    # Vérifie que l'annotation a bien été ajoutée
    assert (
        len(fig2.layout.annotations) == 1
    ), "L'annotation n'a pas été ajoutée correctement."
    assert (
        fig2.layout.annotations[0].text == "Instagram"
    ), "Le texte de l'annotation n'est pas correct."
