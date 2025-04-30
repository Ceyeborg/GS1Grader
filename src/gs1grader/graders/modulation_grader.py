import os
from datetime import datetime
from zoneinfo import ZoneInfo

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from gs1grader.common import (
    DecodedDmtxData,
    get_modulation_attributes,
    map_raw_fit_x_y,
)
from gs1grader.grader_interface import DataMatrixGraderInterface


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
        self.modulation_grades = {}

    def compute_grade(self, decoded_data: DecodedDmtxData) -> str:
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
                    // modulation_attr.symbol_contrast
                )

                # Determine the grade level based on MOD value
                for grade_range in self.grade_thresholds.keys():
                    if mod_value in grade_range:
                        self.modulation_grades[key] = self.grade_thresholds[
                            grade_range
                        ]
                        break

        if self.modulation_grades.values():
            # Find the highest grade for the entire matrix
            return max(self.modulation_grades.values())

        return "F"

    def explain_grade(
        self, decoded_data: DecodedDmtxData, explanation_path: str
    ) -> str:
        """Generate a visual explanation of the modulation grading.

        This method creates a visualization of the DataMatrix with color-coded
        borders indicating the modulation grade of each module.
        The visualization is saved as an image file in the specified path.

        :param decoded_data: Decoded DataMatrix data containing fit
                            coordinates, color values, and matrix dimensions
        :type decoded_data: DecodedDmtxData
        :param explanation_path: Directory path where the explanation image
                            will be saved
        :type explanation_path: str
        :return: The filename of the saved explanation image
        :rtype: str
        """
        timestamp = datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime(
            "%Y%m%d_%H%M%S"
        )
        filename = os.path.join(
            explanation_path, "modulation_grade_" + timestamp
        )

        raw_fit_x_y_dict = map_raw_fit_x_y(decoded_data=decoded_data)
        modulation_grades_raw = {}
        for (x, y), _ in self.modulation_grades.items():
            modulation_grades_raw[
                raw_fit_x_y_dict[(x, y)]
            ] = self.modulation_grades.get((x, y))

        # Set the figure size with gridspec to maintain square grids
        fig, ax = plt.subplots(figsize=(8, 6))

        scatter = ax.scatter(
            decoded_data.raw_x,
            decoded_data.raw_y,
            c=decoded_data.color,
            cmap="viridis",
            marker="s",
            s=50,
            edgecolors="none",
        )
        grade_colors = {
            "A": "lightgreen",
            "B": "lightcoral",
            "C": "indianred",
            "D": "darkorange",
            "F": "darkred",
        }
        # Add borders based on modulation grades
        for key, grade in modulation_grades_raw.items():
            x, y = key
            color = grade_colors.get(grade, "lightgreen")

            rect = plt.Rectangle(
                (x, y), 5, 5, fill=False, edgecolor=color, linewidth=2
            )
            plt.gca().add_patch(rect)

        # Create legend for modulation grades
        legend_handles = [
            mpatches.Patch(edgecolor=color, facecolor="none", label=grade)
            for grade, color in grade_colors.items()
        ]
        plt.legend(
            handles=legend_handles,
            bbox_to_anchor=(1.25, 0.5),
            loc="center left",
            title="Grades",
            frameon=False,
        )
        plt.colorbar(scatter, ax=ax, label="Color Magnitude")
        plt.xlabel("X Coordinates of Modules")
        plt.ylabel("Y Coordinates of Modules")
        plt.title("Explanation of the Modulation grade for given datamatrix")
        plt.xticks(np.arange(0, max(decoded_data.raw_x), 5))
        plt.yticks(np.arange(0, max(decoded_data.raw_y), 5))
        #  plt.xticks(np.arange(0, 5 * (decoded_data.dmtx_size_row + 1), 5))
        #  plt.yticks(np.arange(0, 5 * (decoded_data.dmtx_size_col + 1), 5))

        # plt.grid(True)  # Enable grid lines
        fig.savefig(filename)
        plt.close()

        return filename
