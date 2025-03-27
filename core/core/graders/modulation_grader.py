from datamatrixqa.core.common import DecodedDmtxData, get_modulation_attributes
from datamatrixqa.core.grader_interface import DataMatrixGraderInterface


class ModulationGrader(DataMatrixGraderInterface):
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
        Compute modulation grade based on color values

        Args:
            decoded_data: Contains 'fit_x', 'fit_y', 'color',
                            'size_x', 'size_y',
                          'dmtx_size_row', and 'dmtx_size_col'
        Returns:
            int: Alphabet grade of the modulation grade
        """
        (
            module_x_y,
            module_average,
            symbol_contrast,
            global_threshold,
        ) = get_modulation_attributes(decoded_data)

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
                    (2 * abs(module_average[key] - global_threshold))
                    * 100
                    / symbol_contrast
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
