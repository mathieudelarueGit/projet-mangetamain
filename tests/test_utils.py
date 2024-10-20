import pandas as pd
import pytest
from src.data_loader import DataLoader
from src.utils import filter_dataframebis1  # Assurez-vous que le chemin d'importation est correct


@pytest.fixture
def interactions_data():
    """Simule le chargement des données en utilisant le DataLoader."""
    data_loader = DataLoader()
    df = data_loader.load_data("dataset/RAW_recipes.csv.zip")
    assert not df.empty, "Loaded DataFrame should not be empty"  # Vérifie que le DataFrame n'est pas vide
    return df


def test_filter_dataframebis1_no_matching_results(interactions_data):
    """Test filtering with no matching results."""
    column_names = ["tags"]
    filter_values = ["non-existent-tag"]  # Une valeur qui n'existe pas
    filtered_df = filter_dataframebis1(interactions_data, column_names, filter_values)
    assert len(filtered_df) == 0  # On s'attend à 0 lignes correspondant


def test_filter_dataframebis1_invalid_column(interactions_data):
    """Test filtering with an invalid column name."""
    column_names = ["invalid_column"]  # Une colonne qui n'existe pas
    filter_values = ["value"]
    
    with pytest.raises(KeyError):
        filter_dataframebis1(interactions_data, column_names, filter_values)


def test_filter_dataframebis1_empty_dataframe():
    """Test filtering on an empty DataFrame."""
    df_empty = pd.DataFrame(columns=["tags", "value"])
    column_names = ["tags"]
    filter_values = ["bio"]
    
    filtered_df = filter_dataframebis1(df_empty, column_names, filter_values)
    assert len(filtered_df) == 0  # On s'attend à 0 lignes 


def test_filter_dataframebis1_with_none(interactions_data):
    """Test filtering with None as a filter value."""
    column_names = ["tags"]
    filter_values = [None]  # Vérifie que None est correctement traité
    
    filtered_df = filter_dataframebis1(interactions_data, column_names, filter_values)
    
    # On s'attend à ce qu'il y ait des lignes où la colonne "tags" est None
    assert all(filtered_df["tags"].isnull())  # Toutes les lignes doivent être None


def test_filter_dataframebis1_numeric_filter():
    """Test filtering on a DataFrame with numeric values."""
    df_numeric = pd.DataFrame({
        "n_steps": [1, 2, 3, 4, 5, 6, 7],
        "categories": ["a", "b", "c", "d", "e", "f", "g"],
    })
    column_names = ["n_steps"]
    filter_values = [[1, 2, 3]]
    
    filtered_df = filter_dataframebis1(df_numeric, column_names, filter_values)
    assert len(filtered_df) == 3  


def test_filter_dataframebis1_category_filter():
    """Test filtering on a DataFrame with categorical values."""
    df_categorical = pd.DataFrame({
        "ingredients": pd.Categorical(["eggs", "sugar", "salt", "rabbit", "pepper"]),
    })
    column_names = ["ingredients"]
    filter_values = [["eggs", "pepper"]]
    
    filtered_df = filter_dataframebis1(df_categorical, column_names, filter_values)
    assert len(filtered_df) == 2  











