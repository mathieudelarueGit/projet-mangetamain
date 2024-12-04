import logging
import plotly.express as px
import plotly.graph_objects as go

# Create a logger for the ChartFactory module
logger = logging.getLogger(__name__)


class ChartFactory:
    """
    A factory class for generating various types of Plotly charts.
    """

    @staticmethod
    def pie_chart(
        labels: list, values: list, title: str = "Nutritional Breakdown"
    ) -> go.Figure:
        """
        Generate a pie chart for nutritional data.

        Parameters:
        ----------
        labels : list
            Labels for the pie chart (e.g., "Fat", "Protein").
        values : list
            Corresponding values for the labels.
        title : str, optional
            Title of the chart (default is "Nutritional Breakdown").

        Returns:
        -------
        go.Figure
            A Plotly pie chart figure.
        """
        try:
            fig = px.pie(
                names=labels,
                values=values,
                title=title,
                color=values,
                color_discrete_sequence=px.colors.sequential.Blues[::-1],
                hole=0.7,  # Donut chart
            )
            fig.update_layout(title=dict(text=title, font=dict(size=18)))
            logger.info("Generated pie chart with title '%s'.", title)
            return fig
        except Exception as e:
            logger.error("Failed to generate pie chart: %s", str(e))
            raise

    @staticmethod
    def bar_chart(
        data: px.data,
        x_col: str,
        y_col: str,
        color_col: str,
        text_col: str,
        title: str = "Macronutrient Proportions",
    ) -> go.Figure:
        """
        Generate a stacked bar chart for macronutrient data.

        Parameters:
        ----------
        data : px.data
            Data source for the chart.
        x_col : str
            Column name for the x-axis.
        y_col : str
            Column name for the y-axis.
        color_col : str
            Column name for coloring the bars.
        text_col : str
            Column name for displaying text on bars.
        title : str, optional
            Title of the chart (default is "Macronutrient Proportions").

        Returns:
        -------
        go.Figure
            A Plotly bar chart figure.
        """
        try:
            fig = px.bar(
                data,
                x=x_col,
                y=y_col,
                color=color_col,
                text=text_col,
                barmode="stack",
                title=title,
                labels={"x": "Recipe", "y": "Proportion (%)"},
            )
            fig.update_traces(texttemplate="%{text} Kcal", textposition="outside")
            fig.update_layout(
                showlegend=True,
                xaxis_title=None,
                yaxis_title=None,
                uniformtext_minsize=8,
                uniformtext_mode="hide",
                title=dict(font=dict(size=40)),
            )
            logger.info("Generated bar chart with title '%s'.", title)
            return fig
        except Exception as e:
            logger.error("Failed to generate bar chart: %s", str(e))
            raise

    @staticmethod
    def popularity_chart(
        data: px.data, x_col: str, y_col: str, title: str = "Popularity Over Time"
    ) -> go.Figure:
        """
        Generate a line chart for recipe popularity over time.

        Parameters:
        ----------
        data : px.data
            Data source for the chart.
        x_col : str
            Column name for the x-axis.
        y_col : str
            Column name for the y-axis.
        title : str, optional
            Title of the chart (default is "Popularity Over Time").

        Returns:
        -------
        go.Figure
            A Plotly line chart figure.
        """
        try:
            fig = px.line(
                data,
                x=x_col,
                y=y_col,
                title=title,
                labels={"x": "Date", "y": "Number of Interactions"},
            )
            logger.info("Generated popularity chart with title '%s'.", title)
            return fig
        except Exception as e:
            logger.error("Failed to generate popularity chart: %s", str(e))
            raise

    @staticmethod
    def score_display(mtm_score: int, nutrition: list) -> go.Figure:
        """
        Display a table with the MTM score and nutrition details.

        Parameters:
        ----------
        mtm_score : int
            Healthiness score (e.g., 75).
        nutrition : list
            Nutritional values:
                [calories, fat, sugars, sodium, protein, saturated fat, carbs].

        Returns:
        -------
        go.Figure
            A Plotly table with an annotation for the MTM score.
        """
        try:
            # Determine score color
            if mtm_score < 30:
                score_color = "red"
            elif 30 <= mtm_score < 70:
                score_color = "orange"
            else:
                score_color = "green"

            # Define nutritional labels
            labels = [
                "",
                "",
                "Calories",
                "Total Fat",
                "Sugars",
                "Sodium",
                "Proteins",
                "Saturated Fat",
                "Carbohydrates",
            ]
            table_nutrition = [""] + [""] + nutrition

            # Populate table rows
            rows = [
                labels,
                [
                    f"{value} g" if i > 2 else f"{value} Kcal" if i == 2 else f"{value}"
                    for i, value in enumerate(table_nutrition)
                ],
            ]

            # Create the table
            fig = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=["", ""],  # No header for table cells
                            fill_color="white",
                            align="center",
                            font=dict(family="Source Sans Pro", size=16, color="white"),
                            height=0,
                        ),
                        cells=dict(
                            values=rows,  # Populate table cells with nutrition data
                            fill_color="white",
                            align="center",
                            font=dict(family="Source Sans Pro", size=12, color="black"),
                            height=30,
                            line_color="white",
                        ),
                    )
                ]
            )

            # Add an annotation for the MTM score
            fig.add_annotation(
                text=(
                    "<b>Healthiness Score<br>"
                    f"<span style='color: {score_color};'>{mtm_score}/100</span>"
                    "</b>"
                ),
                x=0.5,  # Centered across the table
                y=1.05,  # Above the table
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=18, color="black", family="Source Sans Pro"),
                align="center",
            )

            # Adjust layout
            fig.update_layout(
                height=400,
                width=400,
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor="white",
            )
            logger.info("Generated score display for MTM score: %d", mtm_score)
            return fig

        except Exception as e:
            logger.error("Failed to generate score display: %s", str(e))
            raise
