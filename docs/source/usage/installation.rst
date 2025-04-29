Installation Guide
==================

Prerequisites
-------------

System Dependencies
~~~~~~~~~~~~~~~~~~~

Before installing GS1Grader, ensure you have the following system dependencies installed:

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

Using the Installation Script from source (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install GS1Grader is using the provided installation script. This script automatically detects your operating system and installs all necessary dependencies:

.. code-block:: bash

    # Clone the repo
    git clone https://github.com/yourusername/GS1Grader.git
    cd GS1Grader

    # Make the script executable
    chmod +x install.sh

    # Run the installation script
    ./install.sh

Using pip
~~~~~~~~~

Alternatively, you can install GS1Grader sdist using pip:

.. code-block:: bash

    pip install gs1grader-x.x.x.tar.gz


Verifying Installation
----------------------

To verify your installation:

.. code-block:: python

    from core.grader_api import DataMatrixGradeAPI

    # Should create instance without errors
    grader = DataMatrixGradeAPI()
