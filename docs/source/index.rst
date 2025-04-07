.. GS1Grader documentation master file, created by
   sphinx-quickstart on Thu Mar 27 09:01:48 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GS1Grader's documentation!
=====================================

GS1Grader is a Python library for grading Data Matrix codes using various quality metrics including modulation and symbol contrast.

Installation
------------

You can install GS1Grader using pip:

.. code-block:: bash

   pip install gs1grader

System Dependencies
-------------------

Before installing, ensure you have the following system dependencies:

.. code-block:: bash

   sudo apt-get install -y \
       libdmtx0b \
       ffmpeg \
       libsm6 \
       libxext6

Quick Start
-----------

Here's a simple example:

.. code-block:: python

   from core.grader_api import DataMatrixGradeAPI

   # Create a grading API instance
   grader_api = DataMatrixGradeAPI()

   # Grade an image using the modulation grader
   grade, explanation = grader_api.grade_datamatrix(
       image_path="path/to/your/datamatrix.jpg",
       grade_type="modulation",
       explain=True
   )

   print(f"Grade: {grade}")
   if explanation:
       print(f"Explanation: {explanation}")

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/grader_api
   api/graders
   api/reader
   usage/installation
   usage/examples
