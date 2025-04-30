from gs1grader.grader_api import DataMatrixGradeAPI

# Simple usage
grader_api = DataMatrixGradeAPI()
for grade in ["modulation", "symbol_contrast"]:
    (grade, explain) = grader_api.grade_datamatrix(
        "./examples/images/datamatrix_2d_original.png", grade, "."
    )
    print(f"Grade: {grade}, Explanation is under: {explain}")
