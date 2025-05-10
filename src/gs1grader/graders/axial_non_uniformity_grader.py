from gs1grader.common import DecodedDmtxData
from gs1grader.grader_interface import DataMatrixGraderInterface


class AxialNonUniformityGrader(DataMatrixGraderInterface):
    """Grader for evaluating the axial non-uniformity of a Data Matrix code.

    Axial non-uniformity measures the consistency of module spacing along
    the horizontal and vertical axes of the Data Matrix. Lower axial
    non-uniformity values indicate more consistent spacing between modules,
    which improves readability and scanning reliability.

    The axial non-uniformity grade is determined by the following thresholds:
    - Grade A: Less than or equal to 6%
    - Grade B: 7% to 8%
    - Grade C: 9% to 10%
    - Grade D: 11% to 12%
    - Grade F: Greater than 12%
    """

    def __init__(self):
        """Initialize the AxialNonUniformityGrader."""
        pass

    def compute_grade(self, decoded_data: DecodedDmtxData):
        """Compute axial non-uniformity grade for the given data matrix
        parameters.

        :param decoded_data: The decoded DataMatrix data containing
                            grid information
        :type decoded_data: DecodedDmtxData
        :returns: The grade of the grid non-uniformity (A, B, C, D, or F)
        :rtype: str
        """
        print("Checkout the advanced version to enable this grade")
        return None

    def explain_grade(self, data):
        """Explain the axial non-uniformity grade for the given data
        matrix parameters.

        :param data: Contains data matrix information and grade
        :type data: DecodedDmtxData
        :returns: Explanation of the grade
        :rtype: str
        """
        print("Checkout the advanced version to enable this grade")
        return None
