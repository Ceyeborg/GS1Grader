Installation Guide
================

Prerequisites
------------

System Dependencies
~~~~~~~~~~~~~~~~~

Before installing GS1Grader, ensure you have the following system dependencies installed:

For Ubuntu/Debian:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y \
        libdmtx0b \
        ffmpeg \
        libsm6 \
        libxext6

For other Linux distributions, install the equivalent packages using your distribution's package manager.

Python Requirements
~~~~~~~~~~~~~~~~

GS1Grader requires Python 3.6 or later.

Installation Methods
------------------

Using pip
~~~~~~~~

The simplest way to install GS1Grader is using pip:

.. code-block:: bash

    pip install gs1grader

From Source
~~~~~~~~~~

To install from source:

.. code-block:: bash

    git clone https://github.com/yourusername/GS1Grader.git
    cd GS1Grader
    pip install -e .


Verifying Installation
-------------------

To verify your installation:

.. code-block:: python

    from core.grader_api import DataMatrixGradeAPI

    # Should create instance without errors
    grader = DataMatrixGradeAPI()
