import plotly.express as px
import plotly.graph_objects as go


class ChartFactory:
    @staticmethod
    def pie_chart(labels, values, title="Nutritional Breakdown"):
        return px.pie(names=labels, values=values, title=title)

    @staticmethod
    def bar_chart(
        data, x_col, y_col, color_col, text_col, title="Macronutrient Proportions"
    ):
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
        )
        return fig

    @staticmethod
    def popularity_chart(data, x_col, y_col, title="Popularity Over Time"):
        fig = px.line(
            data,
            x=x_col,
            y=y_col,
            title=title,
            labels={"x": "Date", "y": "Number of Interactions"},
        )
        return fig

    @staticmethod
    def score_display(mtm_score, nutrition):
        """
        Display a simple table for the score and nutrition details
        with an external black border.

        Parameters:
            mtm_score (int): The calculated score (e.g., 75).
            nutrition (list): Nutritional values
            [calories, fat, sugars, sodium, protein, saturated fat, carbs].
        """
        # Determine qualitative description and color
        if mtm_score < 30:
            # score_text = "Poor"
            score_color = "red"
        elif 30 <= mtm_score < 70:
            # score_text = "Medium"
            score_color = "orange"
        else:
            # score_text = "Good"
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

        # Populate table rows with labels and values
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
                        values=["", ""],  # No visible header for table cells
                        fill_color="white",
                        align="center",
                        font=dict(size=16, color="white"),
                        height=0,
                    ),
                    cells=dict(
                        values=rows,  # Populate table cells with nutrition data
                        fill_color="white",
                        align="center",
                        font=dict(size=12, color="black"),
                        height=30,
                        line_color="white",
                    ),
                )
            ]
        )

        # Add a black border above the first row
        fig.add_shape(
            type="line",
            x0=0.1,
            x1=0.9,
            y0=0.85,  # Position above the first row
            y1=0.85,
            xref="paper",
            yref="paper",
            line=dict(color="black", width=2),
        )

        # Add a black border below the last row
        fig.add_shape(
            type="line",
            x0=0.1,
            x1=0.9,
            y0=0.15,  # Position below the last row (adjust based on table layout)
            y1=0.15,
            xref="paper",
            yref="paper",
            line=dict(color="black", width=2),
        )

        # Add an annotation to display the score
        fig.add_annotation(
            text=(
                "<b>Healthiness Score<br>"
                f"<span style='color: {score_color};'>{mtm_score}/100</span>"
                "</b>"
            ),
            x=0.5,  # Center across the table
            y=1.05,  # Position above the table
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=18, color="black", family="Arial"),
            align="center",
        )

        # Adjust layout
        fig.update_layout(
            height=400,
            width=400,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor="white",
        )

        return fig
