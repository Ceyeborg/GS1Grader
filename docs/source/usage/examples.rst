Usage Examples
==============

Basic Usage
-----------

Simple Grading Example
~~~~~~~~~~~~~~~~~~~~~~

Here's a basic example of grading a Data Matrix code:

.. code-block:: python

    from core.grader_api import DataMatrixGradeAPI

    # Create grader instance
    grader = DataMatrixGradeAPI()

    # Grade an image
    grade, explanation = grader.grade_datamatrix(
        image_path="path/to/image.png",
        grade_type="modulation",
        explain=True
    )

    print(f"Grade: {grade}")
    print(f"Explanation: {explanation}")

Advanced Usage
--------------

Multiple Grading Methods
~~~~~~~~~~~~~~~~~~~~~~~~

Example of using different grading methods:

.. code-block:: python

    grader = DataMatrixGradeAPI()

    # Grade modulation
    mod_grade, mod_explain = grader.grade_datamatrix(
        image_path="path/to/image.png",
        grade_type="modulation",
        explain=True
    )

    # Grade symbol contrast
    contrast_grade, contrast_explain = grader.grade_datamatrix(
        image_path="path/to/image.png",
        grade_type="symbol_contrast",
        explain=True
    )

    print(f"Modulation Grade: {mod_grade}")
    print(f"Symbol Contrast Grade: {contrast_grade}")
