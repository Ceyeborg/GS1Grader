from src.gs1grader.grader_api import DataMatrixGradeAPI


def test_example():
    """
    Example test function to demonstrate the usage of the grading API.
    This function grades a DataMatrix image using the modulation grader.
    """
    # Create a grading API instance
    grader_api = DataMatrixGradeAPI()

    # Grade an image using the modulation grader
    grade, explanation = grader_api.grade_datamatrix(
        image_path="examples/images/datamatrix_2d_8.png",
        grade_type="modulation",
        explanation_path="."
    )

    assert grade is not None, "Grading failed, no grade returned."
    assert explanation is not None, "Grading failed, no explanation returned."
    assert grade == 'D', "Grading failed, expected grade is D."


def test_example_reference():
    """
    Example test function to demonstrate the usage of the grading API.
    This function grades a DataMatrix image using the modulation grader.
    """
    # Create a grading API instance
    grader_api = DataMatrixGradeAPI()

    # Grade an image using the modulation grader
    grade, explanation = grader_api.grade_datamatrix(
        image_path="examples/images/datamatrix_2d_original.png",
        grade_type="modulation",
        explanation_path="."
    )

    assert grade is not None, "Grading failed, no grade returned."
    assert explanation is not None, "Grading failed, no explanation returned."
    assert grade == 'A', "Grading failed, expected grade is A."
