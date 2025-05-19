.. GS1Grader documentation master file, created by
   sphinx-quickstart on Thu Mar 27 09:01:48 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GS1Grader's documentation!
=====================================

GS1Grader is a Python library for grading Data Matrix codes using GS1 quality metrics with modulation and symbol contrast implementation.

Installation Guide
------------------

Prerequisites
-------------

System Dependencies
~~~~~~~~~~~~~~~~~~~

Before installing GS1Grader, please ensure you have the following system dependencies installed:

.. tabs::

    .. tab:: Ubuntu/Debian:

        .. code-block:: bash

            sudo apt-get update
            sudo apt-get install -y \
                libdmtx0b \
                ffmpeg \
                libsm6 \
                libxext6

    .. tab:: Mac OS:

        .. code-block:: bash

            # Install Homebrew if not already installed
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

            # Install required dependencies
            brew install libdmtx
            brew install ffmpeg

For other Linux distributions, install the equivalent packages using your distribution's package manager.

Python Requirements
~~~~~~~~~~~~~~~~~~~

GS1Grader requires Python 3.6 or later.

Installation Methods
--------------------
There are two main ways to install GS1Grader: using pip from PyPI or from the source.
1. **Using pip from PyPI**: This is the recommended method for most users.
2. **From source**: This method is useful for developers or users who want to modify the library.


Using pip from PyPI
~~~~~~~~~~~~~~~~~~~

You can install GS1Grader using pip:

.. code-block:: bash

    pip install gs1grader


From source
~~~~~~~~~~~


.. code-block:: bash

    # Clone the repo
    git clone https://github.com/Ceyeborg/GS1Grader.git
    cd GS1Grader

    poetry install

Verifying the Installation
--------------------------

To verify your installation:

.. code-block:: python

    from gs1grader.grader_api import DataMatrixGradeAPI

    # Should create an DataMatrixGradeAPI instance without errors
    grader = DataMatrixGradeAPI()


Quick Start
-----------

Here's a simple example:

.. code-block:: python

   from gs1grader.grader_api import DataMatrixGradeAPI

   # Create a grading API instance
   grader_api = DataMatrixGradeAPI()

   # Grade an image using the modulation grader
   grade, explanation = grader_api.grade_datamatrix(
       image_path="path/to/your/datamatrix.png",
       grade_type="modulation",
       explanation_path="path/to/explanation_img.png"
   )

   print(f"Grade: {grade}")
   print(f"Explanation is under: {explanation}")

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/grader_api
   api/graders
   api/reader
   usage/examples
