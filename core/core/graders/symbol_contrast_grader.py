from datamatrixqa.core.common import DecodedDmtxData, get_modulation_attributes
from datamatrixqa.core.grader_interface import DataMatrixGraderInterface


class SymbolContrastGrader(DataMatrixGraderInterface):
    def __init__(self):
        self.grade_thresholds = {
            range(70, 256): "A",
            range(55, 70): "B",
            range(40, 55): "C",
            range(20, 40): "D",
            range(0, 20): "F",
        }

    def compute_grade(self, decoded_data: DecodedDmtxData) -> str:
        """
        Compute symbol contrast grade based on color values

        Args:
            decoded_data: Contains 'fit_x', 'fit_y', 'color',
                            'size_x', 'size_y',
                          'dmtx_size_row', and 'dmtx_size_col'
        Returns:
            str: Alphabet grade of the symbol contrast
        """
        (
            module_x_y,
            module_average,
            symbol_contrast,
            global_threshold,
        ) = get_modulation_attributes(decoded_data)

        for symbol_contrast_range, grade in self.grade_thresholds.items():
            if symbol_contrast in symbol_contrast_range:
                return grade

        return "F"

    def explain_grade(self, data):
        return super().explain_grade(data)
