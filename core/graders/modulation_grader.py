from core.common import DecodedDmtxData, get_modulation_attributes
from core.grader_interface import DataMatrixGraderInterface


class ModulationGrader(DataMatrixGraderInterface):
    """Grader for evaluating the modulation quality of a Data Matrix code.

    Modulation measures the contrast between light and dark modules in
    the Data Matrix. Higher modulation values indicate better contrast
    between modules, which improves readability and scanning reliability.

    The modulation grade is determined by the following thresholds:
    - Grade A: 50% or higher
    - Grade B: 40% to 50%
    - Grade C: 30% to 40%
    - Grade D: 20% to 30%
    - Grade F: Less than 20%
    """

    def __init__(self):
        self.grade_thresholds = {
            range(50, 256): "A",
            range(40, 50): "B",
            range(30, 40): "C",
            range(20, 30): "D",
            range(0, 20): "F",
        }

    def compute_grade(self, decoded_data: DecodedDmtxData) -> int:
        """
        Compute modulation grade based on color values.

        This method calculates the modulation grade by analyzing the contrast
        between light and dark modules in the DataMatrix code.

        :param decoded_data: The decoded DataMatrix data containing:
            - fit_x: X coordinates of the fitted grid points
            - fit_y: Y coordinates of the fitted grid points
            - color: Color values at each grid point
            - dmtx_size_row: Number of rows in the DataMatrix
            - dmtx_size_col: Number of columns in the DataMatrix
        :type decoded_data: DecodedDmtxData
        :returns: The grade of the modulation (A, B, C, D, or F)
        :rtype: str
        """
        modulation_attr = get_modulation_attributes(decoded_data)

        module_x_y = modulation_attr.module_x_y
        # remove empty modules
        module_x_y = {
            key: module_x_y[key]
            for key in module_x_y
            if len(module_x_y[key]) != 0
        }

        modulation_grades = {}
        for key in module_x_y:
            if (
                key[0] > -1
                and key[1] > -1
                and key[0] < decoded_data.dmtx_size_row
                and key[1] < decoded_data.dmtx_size_col
            ):
                # Calculate MOD value
                mod_value = (
                    (
                        2
                        * abs(
                            modulation_attr.module_average[key]
                            - modulation_attr.global_threshold
                        )
                    )
                    * 100
                    / modulation_attr.symbol_contrast
                )

                # Determine the grade level based on MOD value
                for grade_range, grade_level in self.grade_thresholds.items():
                    if mod_value in grade_range:
                        grade_level = self.grade_thresholds[mod_value]

                modulation_grades[key] = grade_level

        # Find the highest grade for the entire matrix
        grade = max(modulation_grades.values())

        return grade

    def explain_grade():
        pass
