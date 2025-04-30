from gs1grader.grader_interface import DataMatrixGraderInterface


class DataMatrixGraderFactory:
    """
    Factory class for creating Data Matrix graders.

    This class implements the factory pattern to create appropriate graders
    based on the requested grade type. It maintains a registry of available
    graders and provides methods to register new graders and retrieve
    instances of registered graders.

    :param _graders: Dictionary mapping grader names to grader classes.
    :type _graders: dict

    :example:

    >>> # Create a factory
    >>> factory = DataMatrixGraderFactory()
    >>>
    >>> # Register graders
    >>> factory.register_grader("modulation", ModulationGrader)
    >>> factory.register_grader("symbol_contrast", SymbolContrastGrader)
    >>>
    >>> # Get a grader instance
    >>> modulation_grader = factory.get_grader("modulation")
    """

    def __init__(self):
        self._graders = {}

    def register_grader(
        self, grader_name: str, grader_class: DataMatrixGraderInterface
    ):
        assert issubclass(
            grader_class, DataMatrixGraderInterface
        ), "Grader must implement DataMatrixGraderInterface"
        self._graders[grader_name] = grader_class

    def get_grader(self, grader_name: str) -> DataMatrixGraderInterface:
        grader = self._graders.get(grader_name)
        if not grader:
            raise ValueError(f"Grader {grader_name} not found")
        return grader()
