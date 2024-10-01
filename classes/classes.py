import pandas as pd
import logging


# configure logging
logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)


class Functions:

    # constructeur
    def __init__(self) -> None:
        pass

    @staticmethod
    # renvoyer les 5 premières lignes du
    def head_dataframe(path_to_dataframe: str) -> str:
        """_summary_
        This method is called to display the first 5 lines of any Dataframe.
        The dataframe is refered to its relative path as the sole argument.
        Returns:
            str: equivalent to df.head()
        """

        try:
            df = pd.read_csv(path_to_dataframe)
        except Exception as e:
            # TODO: log the error in the notebook
            logging.error(
                f"Erreur lors de la lecture du fichier CSV spécifié à  \ l'emplacement {path_to_dataframe}: {e}"
            )
            print(e)

        to_display = df.head().to_string()
        return to_display
