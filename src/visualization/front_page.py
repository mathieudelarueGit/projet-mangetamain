import streamlit as st

def render_front_page():
    """
    Render the front page of the app when no recipes are displayed.
    """
    tabs = st.tabs(["App purpose", "Data processing behind the scene"])
    with tabs[0]:
        # Add a banner image (use a relative path to assets directory)
        st.image(
            "src/visualization/images/mangetamain_front_page_banner.jpg",
            use_column_width=True,
        )

        # Welcome text with HTML for styling
        st.markdown(
            """
            <div class="opaque-background">
                <h1>Welcome to Mangetamain!</h1>
                <p>
                    A web app designed to help you cook healthy recipes
                    depending on what is available in your fridge.
                </p>
                <p>
                    At Mangetamain, you will only find traditional bio
                    recipes that will make you healthier! We retrieved only recipes
                    that our dear contributors rated minimum 4 stars,
                    so you won't be disappointed!
                </p>
                <p>
                    Just select which ingredients you have in your fridge,
                    and we will propose you the best recipes there is for you.
                    You can even filter by macronutrients if you are on a specific diet
                    or you just care about what's inside your plate!
                </p>
                <p>
                    In doubt, you can always refer to the MTM score,
                    an in-house score specifically designed to help
                    you assess the quality of the recipe.
                </p>
                <h2>Have fun!</h2>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with tabs[1]:
        st.header("Sélection des recettes")
        st.write(
            """
                    **Cibler des recettes "healthy" et éthiques** \n
                    Le fichier RAW recipes contient tout un nombre de recettes qui ne
                    correspondent pas à notre objectif de suggérer des recettes qui
                    soient "healthy". Pour cibler les recettes d'intéret pour nous,
                    nous avons filtré selon les données de la colonne "tag" et avons
                    retenus arbitrairement les recettes comportant les mentions:
                    organic, bio, clean, vegetable, vegan, traditional, eco-friendly,
                    local, healthy, seasonal, green, natural, fresh, plant,
                    sustainable, heritage, garden, whole, farm.
                """
        )
        st.write(
            """
                    **Pertinence des reviews** \n
                    Dans RAW_interactions, nous constatons que les notes des recettes
                    sont trop élevées pour qu'une étude se base sur ce critère.
                """
        )
        st.image("src/visualization/images/ratings.png", use_column_width=True)
        st.write(
            """
                    En outre, toutes les recettes ayant une note inférieure à 4
                    sont considérées comme de mauvaises recettes, car les utilisateurs
                    ont tendance à attribuer des notes très élevées en général. Nous
                    filtrons donc les recettes ayant une note strictement inférieure à
                    4, nous considérons que ce sont de mauvaises recettes.
                """
        )
        st.write(
            """
                    **Temps de préparation** \n
                    Nous procédons ensuite à l'analyse des temps de préparation. Nous
                    ciblons des personnes actives, soucieuses de leur mode de vie,
                    mais qui ont un temps limité pour cuisiner. Nos utilisateurs
                    souhaitent probablement passer moins de 2 heures au fourneau !
                """
        )
        st.image(
            "src/visualization/images/preparation_time.png",
            use_column_width=True)
        st.write(
            """
                    De plus, nous considérons que les recettes de moins de 5 minutes
                    sont des erreurs de saisie ou peu sérieuses. Par conséquent, nous
                    filtrons les recettes dont le temps de préparation est inférieur à
                    5 minutes.
                """
        )
        st.write(
            """
                    **Vectorisation des ingrédients** \n
                    Nous utilisons le fichier pickle pour réécrire la liste des
                    ingrédients sous forme de texte. Ensuite, nous appliquons Word2Vec
                    pour obtenir les vecteurs denses des ingédients. Lorsqu'un
                    ingrédient est décrit avec plusieurs mots, nous le représentons
                    par le vecteur moyen de ses mots. Notre dataset contient plus de
                    6000 ingrédients uniques. A l'aide de Word2Vec nous récupérons la
                    déisgnation simple la plus proche de l'ingrédient original. Nous
                    réduisons ainsi le nombre d'ingrédients uniques à environ 1200,
                    ce qui constitue une simplification très significative.
                """
        )
        st.image(
            "src/visualization/images/word2vec.png",
            use_column_width=True)
        st.write(
            """
                    Le nombre d'ingrédients par recette suit une loi de type loi gamma.
                    La rationnalisation de la désignation des ingrédients permets
                    d'analyser les ingrédients les plus utilisés dans les recettes.
                    Les condiments sont surreprésentés, ils ne caractérisent pas les
                    recettes. Au passage, la liste des 40 ingrédients ci-dessous
                    illustre le must-have pour cuisiner des recettes plus saines.
                """
        )
        st.image(
            "src/visualization/images/top-ingredients.png",
            use_column_width=True)
        st.write(
            """
                    **Composition nutritionnelle** \n
                    La composition nutruitionnelle est un élément clé pour répondre
                    à notre problématique. Les macronutriments sont initialement
                    exprimés en pourcentage des apports journaliers recommandés.
                    Nous convertissons ces valeurs en grammes et recalculons l'apport
                    calorique pour chaque recette, en appliquant la règle suivante:
                    -1 gramme de protéines = 4 kcal
                    -1 gramme de glucides = 4 kcal
                    -1 gramme de lipides = 9 kcal
                    Nous éliminons également les recettes pour lesquelles les valeurs
                    nutritionnelles sont manquantes (0) ou hors-cible (> 3150).
                """
        )
        st.write(
            """
                    **Dataset final** \n
                    Avec en tête ce que l'application doit fournir, nous décidons
                    de ne conserver que les informations suivantes dans le dataset :
                    - nom de recette
                    - numério identification
                    - composition nutritionnelle
                    - liste des ingrédients
                """
        )
