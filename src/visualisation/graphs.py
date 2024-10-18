import pandas as pd
import plotly.express as px

from src.data_loader import DataLoader

# Loads the raw interactions dataset using the data_loader module
data_loader = DataLoader()
# interactions = data_loader.load_data("dataset/RAW_interactions.csv.zip")
interactions = data_loader.load_data("dataset/RAW_interactions.csv.xz")

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
fig2 = px.histogram(interactions.date, title="Dynamics in time")

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

# Creates a scatter plot showing the interaction counts for each recipe
fig3 = px.scatter(
    interactions.recipe_id.value_counts(), title="Too popular to be serious"
)


fig3.add_annotation(
    text="Buzzing zone",
    x=197730,  # x position in the range (adjust as needed)
    y=1000,  # y position (80% of the curve height)
    showarrow=False,
    font=dict(size=15, color="black"),
    bgcolor="rgba(255, 255, 255, 0.7)",  # Semi-transparent white background
    bordercolor="black",
    borderwidth=1,
    borderpad=4,
)

fig3.update_layout(
    xaxis_title="All recipes stored",  # x-axis label (commented out)
    yaxis_title="Number of interactions for each recipe",  # y-axis label
    showlegend=False,  # Hides the legend
    xaxis=dict(
        tickvals=[],  # No tick values shown on the x-axis
        showline=False,  # Do not show the x-axis line
    ),
)

# Adds a transparent rectangle to highlight the area above 500 interactions
fig3.add_shape(
    type="rect",
    x0=fig3.data[0].x.min(),  # Start position on x (min value of the x-axis)
    x1=fig3.data[0].x.max(),  # End position on x (max value of the x-axis)
    y0=500,  # Start position on y (500)
    y1=fig3.data[0].y.max(),  # End position on y (max value of the y-axis)
    line=dict(color="rgba(255, 0, 0, 0)"),  # No visible border
    fillcolor="rgba(255, 0, 0, 0.2)",  # Transparent red fill
)
