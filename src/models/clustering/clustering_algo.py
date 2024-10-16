import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import re
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from base import *
from log_config import *
from data_loader import *
#from src.models.clustering.clustering_algo import ClusteringModel


class ClusteringModel(BaseClustering):
    """
    A class that performs DBSCAN clustering on nutritional data.
    """

    def __init__(self, eps: float, min_samples: int):
        """
        Initialize the ClusteringModel with DBSCAN parameters.

        Args:
            eps (float): DBSCAN's epsilon parameter (max distance for clustering).
            min_samples (int): Minimum number of samples to form a core point.
        """
        self.eps = eps
        self.min_samples = min_samples
        self.scaler = StandardScaler()
        self.dbscan_model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        self.clusters = None
        self.nutrition_data_scaled = None

    def parse_nutrition(self, nutrition_str: str) -> np.ndarray:
        """
        Convert a string of nutrition facts to a NumPy array.

        Args:
            nutrition_str (str): Nutrition data string (e.g., "[100, 10, 5, 300, ...]").
        
        Returns:
            np.ndarray: Parsed nutrition data or NaN if parsing fails.
        """
        try:
            return np.array(ast.literal_eval(nutrition_str))
        except ValueError:
            return np.array([np.nan]*7)

    def fit(self, df_filtered_bio: pd.DataFrame) -> None:
        """
        Fit the DBSCAN clustering model on nutrition data.

        Args:
            df_filtered_bio (pd.DataFrame): DataFrame containing nutrition data.
        """
        # Parse and prepare nutrition data
        nutrition_data = df_filtered_bio['nutrition'].dropna().apply(self.parse_nutrition)
        nutrition_df = pd.DataFrame(nutrition_data.tolist(), columns=[
            'Calories', 'Total Fat (g)', 'Sugar (g)', 'Sodium (mg)', 
            'Protein (g)', 'Saturated Fat (g)', 'Carbohydrates (g)'
        ])
        
        # Standardize the data
        self.nutrition_data_scaled = self.scaler.fit_transform(nutrition_df)
        
        # Fit DBSCAN model
        self.clusters = self.dbscan_model.fit_predict(self.nutrition_data_scaled)
        nutrition_df['cluster'] = self.clusters

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict the cluster labels for new data points.

        Args:
            X (np.ndarray): New input data for prediction.

        Returns:
            np.ndarray: Predicted cluster labels.
        """
        X_scaled = self.scaler.transform(X)
        return self.dbscan_model.fit_predict(X_scaled)

    def plot_clusters(self, nutrition_df: pd.DataFrame, clusters: np.ndarray, x: str, y: str, xlabel: str, ylabel: str, title: str, filename: str) -> None:
        """
        Create and save a scatter plot of the clusters.

        Args:
            nutrition_df (pd.DataFrame): DataFrame of nutrition data with cluster labels.
            clusters (np.ndarray): Cluster labels.
            x (str): Feature for the x-axis.
            y (str): Feature for the y-axis.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Plot title.
            filename (str): Path to save the plot.

        Returns:
            None: Saves the plot to the specified file path.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=nutrition_df[x], y=nutrition_df[y], hue=clusters, palette='viridis', legend='full')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(filename)
        plt.show()
    # Initialize and fit the model
    # Assuming df_filtered_bio is the DataFrame with features (X) and target (y)

X = df_filtered_bio.drop(columns=['target']).values
y = df_filtered_bio['target'].values
model = ClusteringModel(eps=2, min_samples=9)
model.fit(df_filtered_bio)
y_pred = model.predict(X)
r2 = model.evaluate(y, y_pred)
print(f"R-squared: {r2}")
model.plot_clusters('Feature 1', 'Feature 2')
