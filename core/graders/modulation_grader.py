from core.grader_interface import DataMatrixGraderInterface

class ModulationGrader(DataMatrixGraderInterface):
    def __init__(self):
        self.grade_thresholds = {
            range(50, 256): 'A',
            range(40, 50): 'B',
            range(30, 40): 'C',
            range(20, 30): 'D',
            range(0, 20): 'F'
        }

    
    def compute_grade(self, data):
        """
        Compute modulation grade based on color values
        
        Args:
            data (dict): Contains 'color_values' and other necessary parameters
        Returns:
            dict: Grade information including letter grade and score
        """
        color_values = data['color_values']
        modulation_score = self._calculate_modulation(color_values)
        grade = self._determine_grade(modulation_score)
        
        return {
            'grade': grade,
            'score': modulation_score,
            'name': "Modulation"
        }

    def explain_grade() -> Path: