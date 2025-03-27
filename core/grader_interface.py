from abc import ABC, abstractmethod

class DataMatrixGraderInterface(ABC):
    @abstractmethod
    def compute_grade(self, data):
        """Compute grade for the given data matrix parameters"""
        pass

    @abstractmethod
    def explain_grade(self, data):
        """Explain the grade for the given data matrix parameters"""
        pass

