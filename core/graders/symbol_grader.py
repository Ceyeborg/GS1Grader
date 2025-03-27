from core.grader_interface import DataMatrixGraderInterface

class SymbolContrastGrader(DataMatrixGraderInterface):
    def __init__(self)
        self.grade_thresholds = {
            range(70, 256): 'A',
            range(55, 70): 'B',
            range(40, 55): 'C',
            range(20, 40): 'D',
            range(0, 20): 'F'
        }

    def compute_grade(self, data):