from abc import ABC, abstractmethod


class DataMatrixGraderInterface(ABC):
    """
    Interface for Data Matrix graders.

    This abstract base class defines the interface that all Data Matrix graders
    must implement. Graders are responsible for evaluating specific quality
    aspects of Data Matrix codes and providing both a grade and an explanation
    of that grade.

    Example:
        ```python
        class ModulationGrader(DataMatrixGraderInterface):
            def compute_grade(self, decoded_data):
                # Implementation of modulation grading
                return grade_value

            def explain_grade(self, data):
                # Explanation of how the grade was determined
                return explanation
        ```

    Attributes:
        None
    """

    @abstractmethod
    def compute_grade(self, decoded_data):
        """Compute grade for the given data matrix parameters"""
        pass

    @abstractmethod
    def explain_grade(self, decoded_data, explanation_path):
        """Explain the grade for the given data matrix parameters"""
        pass
