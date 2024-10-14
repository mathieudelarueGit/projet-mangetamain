class Algorithm:
    """
    A base class for different algorithms, storing the algorithm's
    name and parameters.

    Attributes:
        name (str): The name of the algorithm.
        params (dict): A dictionary of parameters for the algorithm.
        Defaults to an empty dictionary if not provided.
    """

    def __init__(self, name: str, params: dict = None):
        """
        Initialize the Algorithm with a name and optional parameters.

        Args:
            name (str): The name of the algorithm.
            params (dict, optional): A dictionary of parameters for the algorithm.
            Defaults to None, which initializes an empty dictionary.
        """
        self.name = name
        self.params = params if params else {}

    def set_param(self, param_name: str, param_value: any) -> None:
        """
        Set or update a parameter in the algorithm's parameters dictionary.

        Args:
            param_name (str): The name of the parameter to set.
            param_value (any): The value of the parameter.
        """
        self.params[param_name] = param_value

    def get_param(self, param_name: str) -> any:
        """
        Retrieve the value of a parameter by its name.

        Args:
            param_name (str): The name of the parameter to retrieve.

        Returns:
            any: The value of the parameter if it exists, otherwise None.
        """
        return self.params.get(param_name, None)

    def model_info(self) -> dict:
        """
        Return a summary of the algorithm's name and parameters.

        Returns:
            dict: A dictionary containing the name of the algorithm
            and its parameters.
        """
        return {
            "name": self.name,
            "params": self.params,
        }
