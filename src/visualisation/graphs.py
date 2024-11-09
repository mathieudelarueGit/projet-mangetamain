import pandas as pd
import plotly.express as px

from src.data_loader import DataLoader

# Loads the raw interactions dataset using the data_loader module
data_loader = DataLoader()
# interactions = data_loader.load_data("dataset/RAW_interactions.csv.zip")
interactions = data_loader.load_data("dataset/RAW_interactions.csv.xz")
interactions_preprocessed = data_loader.load_data(
    "preprocessed_data/PP_interactions_mangetamain.csv"
)
# Creates a DataFrame with the count of each rating in the interactions dataset
ratio_of_ratings = pd.DataFrame(interactions.rating.value_counts())
ratio_of_ratings.columns = ["count"]  # Renaming the column to 'count'
# The top 10 most popular recipes (commented out alternative approach)
with open("src/visualisation/top10_hottest_recipes.txt") as f:
    top10_hottest_recipes = f.read()

# Adds a 'ratio' column to store the ratio of each rating relative to the total count
ratio_of_ratings["ratio"] = ratio_of_ratings["count"] / ratio_of_ratings["count"].sum()

# Creates a pie chart representing the distribution of ratings
fig1 = px.pie(
    ratio_of_ratings,
    names=ratio_of_ratings.index,  # Uses the index (ratings) as labels
    values="count",  # Uses the 'count' column for segment sizes
    title="Ratio of ratings in the dataset",
    color=ratio_of_ratings.index,  # Uses the index to set the color
    color_discrete_sequence=px.colors.sequential.Blues[
        ::-1
    ],  # Shades from light to dark blue
)

# Updates the layout of the pie chart to display both percentage and label
fig1.update_traces(textinfo="label+percent")


# Creates a histogram to show the dynamics of interactions over time
fig2 = px.histogram(interactions_preprocessed.date, title="Dynamics in time")

fig2.add_annotation(
    text="Instagram",
    x="2012-01-31",  # x position in the time interval (adjust as needed)
    y=6000,  # y position (adjust as needed)
    showarrow=False,
    font=dict(size=15, color="black"),
    bgcolor="rgba(255, 255, 255, 0.7)",  # Semi-transparent white background
    bordercolor="black",
    borderwidth=1,
    borderpad=4,
)

# Updates the labels of the axes
fig2.update_layout(
    xaxis_title="Time",  # x-axis label
    yaxis_title="Amount of interactions",  # y-axis label
    showlegend=False,  # Disable the legend
)
fig3 = px.violin(
    interactions_preprocessed.recipe_id.value_counts(),
    title="Too popular to be serious",
)

# Update the appearance to enhance visibility of the wings
fig3.update_traces(
    side="positive",  # Ensure the violin is directed to one side
    width=0.9,  # Adjust the violin's width
    opacity=0.5,  # Reduce opacity to make violins more transparent
    jitter=0.05,  # Apply a slight offset to better visualize points
    spanmode="hard",  # Reduce smoothing for more detailed visualization
)

# Adjust the axes for better visibility of variations
fig3.update_layout(
    yaxis_title="Number of interactions for each recipe",  # y-axis title
    xaxis_title="Recipe ID",  # Add a title to the x-axis
    yaxis=dict(
        range=[
            0,
            interactions_preprocessed.recipe_id.value_counts().max() + 100,
        ],  # Set y-axis range for better visibility
        tickmode="linear",  # Linear tick mode for a uniform scale
    ),
    xaxis=dict(
        showticklabels=False,  # Hide x-axis labels
        showline=False,  # Hide x-axis line
    ),
    showlegend=False,  # Hide legend
)

# Add an annotation in the buzzing zone
fig3.add_annotation(
    text="Buzzing zone",
    x=0,  # x position within the range (adjust if needed)
    y=600,  # y position (80% of the curve height)
    showarrow=False,
    font=dict(size=15, color="black"),
    bgcolor="rgba(255, 255, 255, 0.7)",  # Semi-transparent white background
    bordercolor="black",
    borderwidth=1,
    borderpad=4,
)

# Add a transparent shape to mark the area above 500 interactions
fig3.add_shape(
    type="rect",
    x0=fig3.data[0].x.min(),  # Starting x position
    x1=fig3.data[0].x.max(),  # Ending x position
    y0=10,  # Starting y position (500 interactions)
    y1=500,  # Maximum y position
    line=dict(color="rgba(255, 0, 0, 0)"),  # No visible border
    fillcolor="rgba(255, 0, 0, 0.2)",  # Transparent red fill color
)
# Further enhance violin visibility by adjusting width
fig3.update_traces(
    side="positive",  # May help make distributions clearer
    width=0.8,  # Width of the violin shape, adjust as needed
)
