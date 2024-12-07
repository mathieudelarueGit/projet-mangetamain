# Mangetamain - Healthy Recipe Recommendation App

Welcome to **Mangetamain**, a streamlit web app designed to help you cook healthy recipes depending on what is available in your fridge. At Mangetamain, you will only find traditional bio recipes that are guaranteed to make you healthier!

This project was made from a dataset consisting of 180K+ recipes and 700K+ recipe reviews covering 18 years of user interactions and uploads on Food.com (formerly GeniusKitchen): https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions

## Features

- **Smart Recipe Selection**: Only healthy and ethical recipes based on specific tags like "organic", "bio", "vegan", "sustainable", and more.
- **User Reviews**: All recipes have been rated at least 4 stars by contributors, ensuring high-quality recommendations.
- **Ingredient-based Search**: Just select what ingredients you have in your fridge, and we'll recommend the best recipes for you.
- **Macronutrient Filters**: Filter recipes based on macronutrients if you're following a specific diet.
- **MTM Score**: Refer to the MTM score, an in-house scoring system to assess the quality of recipes.
- **Seasonal Recipes**: The app recommends recipes that are in season for better sustainability and freshness.

## How to Use

- **Select Ingredients**: Log in to the app and choose what ingredients you have available in your fridge.
- **Filter Recipes**: Use the filters to select your desired macronutrient values, cooking time, and seasonality preferences.
- **Browse Recipes**: View the recommended recipes, along with nutritional details and the MTM score.
- **Cook**: Once you’ve found a recipe, get cooking and enjoy a healthy meal!

## Installation

### Prerequisites

Before getting started, ensure you have the following dependencies installed:

- Python 3.x
- pip (Python package manager)

### Steps

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/mangetamain.git
   cd mangetamain
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
4. Run the web app locally:
   ```bash
   streamlit run src/main.py

## Dataset & Methodology

The Mangetamain application runs on a dataset that was made out the orgiginal Food.com data through a singular datamining process. The dataset in question is included in the project, so you don't have to do the job yourself. The whole process is explained down below. 

### Recipe Selection Criteria

To provide users with healthy and ethical recipes, the following filters were applied:

- **Tagging**: Recipes were filtered based on specific tags such as *organic, bio, vegan, seasonal*, etc. Recipes not meeting these criteria were excluded.
- **Rating**: Recipes with a rating below 4 stars were filtered out to ensure only high-quality recipes are recommended.
- **Preparation Time**: Recipes with preparation times less than 5 minutes or more than 2 hours were excluded to meet the target audience’s preferences for quick, healthy meals.

### Ingredient Vectorization

The ingredients in the recipes are processed using Word2Vec, which transforms ingredient descriptions into dense vectors. This allows the app to simplify over **6000 unique ingredients** into a more manageable list of approximately **1200 unique ingredients** for better recipe matching.

### Nutritional Composition

The nutritional data (macronutrients) is processed and converted into grams, and the calorie content is recalculated based on the following:
- 1 gram of protein = 4 kcal
- 1 gram of carbohydrate = 4 kcal
- 1 gram of fat = 9 kcal

Recipes with missing or incorrect nutritional information are excluded.

### Seasonality Analysis

A key feature of Mangetamain is the ability to suggest recipes based on seasonality. Recipes are analyzed using the dates of their reviews, and seasonal trends are detected using the following method:
- Mapping of review dates to an angle between 0 and 2π.
- Calculation of mean and standard deviation for the sine and cosine values of these angles to assess the seasonality.
- Recipes with a high seasonality score are prioritized in the app's recommendations.

# Contributing

We welcome contributions to the project! If you want to report a bug, suggest a feature, or submit a pull request, feel free to open an issue or create a pull request.

# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments

- **Food.com Dataset**: Our app is powered by a rich dataset of recipes and user reviews, sourced from Food.com (formerly GeniusKitchen).
- **Word2Vec**: We used Word2Vec to vectorize the ingredients for more accurate recipe matching.
- **Seasonality Analysis**: Special thanks to the contributors who helped in analyzing seasonal trends in recipes.

# Documentation

The project documentation is available online at the following link:

[Click here for the documentation](https://mathieudelaruegit.github.io/projet-mangetamain)
