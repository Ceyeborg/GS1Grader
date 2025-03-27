from datamatrixqa.core.grader_interface import DataMatrixGraderInterface


class DataMatrixGraderFactory:
    def __init__(self):
        self._graders = {}
    
    def register_grader(self, grader_name: str, grader_class: DataMatrixGraderInterface):
        assert issubclass(grader_class, DataMatrixGraderInterface), "Grader must implement DataMatrixGraderInterface"
        self._graders[grader_name] = grader_class
    
    def get_grader(self, grader_name: str):
        grader = self._graders.get(grader_name)
        if not grader:
            raise ValueError(f"Grader {grader_name} not found")
        return grader()
