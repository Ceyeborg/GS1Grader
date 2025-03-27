from datamatrixqa.core.grader_api import DataMatrixGradeAPI

# Simple usage
grader_api = DataMatrixGradeAPI()
(grade, explain) = grader_api.grade_datamatrix(
    "./examples/images/datamatrix_2d_8.png", "modulation"
)
print(f"Grade: {grade}, Explanation: {explain}")
