from gs1grader.grader_interface import DataMatrixGraderInterface


class UECGrader(DataMatrixGraderInterface):
    """
    Grader for Unused Error Correction (UEC) in Data Matrix codes.

    This grader evaluates the amount of unused error correction capacity
    in a Data Matrix code. Higher unused error correction indicates better
    robustness against potential damage or scanning issues.

    The UEC grade is determined by the percentage of error correction capacity
    that remains unused in the Data Matrix code. A higher percentage results
    in a better grade, indicating more resilience against errors.

    The UEC grade is determined by the following thresholds:
    - Grade A: Greater than or equal to 62% unused error correction
    - Grade B: 50% to 61% unused error correction
    - Grade C: 37% to 49% unused error correction
    - Grade D: 25% to 36% unused error correction
    - Grade F: Less than 25% unused error correction
    """

    def compute_grade(self, decoded_data):
        """
        Compute the Unused Error Correction (UEC) grade for the
        given data matrix.

        This method calculates the grade based on the percentage of unused
        error correction capacity in the Data Matrix code.

        :param decoded_data: Contains decoded Data Matrix information
        :type decoded_data: DecodedDmtxData
        :return: The grade of the unused error correction (A, B, C, D, or F)
        :rtype: str

        :GS1: The grade is determined by the percentage of error correction
              capacity that remains unused. Grade A (4.0) indicates high
              unused capacity, while Grade F (0.0) indicates little to no
              unused capacity.
        """
        print("Checkout our advanced version to enable this grade")
        return None

    def explain_grade(self, data):
        """
        Provide an explanation for the UEC grade of the given
        data matrix parameters.

        :param data:
        :type data: DecodedDmtxData
        :return: Explanation of the grade
        :rtype: str
        """
        print("Checkout our advanced version to enable this grade")
        return None
