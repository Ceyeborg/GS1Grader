Usage Examples
==============

This section provides examples of how to use the GS1 Grader package. We recommend starting with the interactive Jupyter notebook example below, which provides a hands-on introduction to the package's features.

Interactive Examples
--------------------

The following Jupyter notebook provides interactive examples with real outputs and visualizations:

.. toctree::
   :maxdepth: 2

   notebooks/examples

Basic Usage
-----------

Simple Grading Example
~~~~~~~~~~~~~~~~~~~~~~

Here's a basic example of grading a Data Matrix code:

.. code-block:: python

    from gs1grader.grader_api import DataMatrixGradeAPI

    # Create grader instance
    grader = DataMatrixGradeAPI()

    # Grade an image
    grade, explanation = grader.grade_datamatrix(
        image_path="path/to/image.png",
        grade_type="modulation",
        exaplanation_path="path/to/explanation_img"
    )

    print(f"Grade: {grade}")
    print(f"Explanation is under: {explanation}")

Advanced Usage
--------------

Multiple Grading Methods
~~~~~~~~~~~~~~~~~~~~~~~~

Example of using different grading methods:

.. code-block:: python

    from gs1grader.grader_api import DataMatrixGradeAPI

    grader = DataMatrixGradeAPI()
    grade_types=["modulation", "symbol_contrast"]

    for grade_type in grade_types:
        grade, exaplanation = grader.grade_datamatrix(
            image_path="path/to/image.png",
            grade_type=grade_type,
            exaplanation_path="path/to/expalantion_img"
        )
        print(f"For {grade_type} -> Grade: {grade}")
        print(f"For {grade_type} -> Explanation is under: {exaplanation}")
