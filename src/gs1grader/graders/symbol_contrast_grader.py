from gs1grader.common import DecodedDmtxData, get_modulation_attributes
from gs1grader.grader_interface import DataMatrixGraderInterface


class SymbolContrastGrader(DataMatrixGraderInterface):
    """Grader for evaluating the symbol contrast of a Data Matrix code.

    Symbol contrast measures the difference between the reflectance of
    light and dark modules in the Data Matrix. Higher symbol contrast
    values indicate better differentiation between light and dark modules,
    which improves readability and scanning reliability.

    The symbol contrast grade is determined by the following thresholds:
    - Grade A: 70% or higher
    - Grade B: 55% to 70%
    - Grade C: 40% to 55%
    - Grade D: 20% to 40%
    - Grade F: Less than 20%
    """

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
        Compute symbol contrast grade based on color values.

        Symbol contrast is the difference between the reflectance
        of light and dark modules. This method calculates the
        symbol contrast value and determines the grade based on
        predefined thresholds.

        :param decoded_data: The decoded DataMatrix data containing
                             information about the modules and their
                             color values.
        :type decoded_data: DecodedDmtxData

        :returns: The grade of the symbol contrast (A, B, C, D, or F).
        :rtype: str
        """
        modulation_attr = get_modulation_attributes(decoded_data)

        for symbol_contrast_range, grade in self.grade_thresholds.items():
            if int(modulation_attr.symbol_contrast) in symbol_contrast_range:
                return grade

        return "F"

    def explain_grade(
        self, decoded_data: DecodedDmtxData, explanation_path: str
    ):
        print("No explanation for symbol contrast")
