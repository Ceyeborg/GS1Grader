# GS1Grader

![Banner](GitHub%20Header-UDI.jpg)

GS1Grader is a Python library for grading Data Matrix codes using GS1 quality metrics with modulation and symbol contrast implementation.

## Prerequisites

Before installing GS1Grader, you need to install some system dependencies:


### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y \
    libdmtx0b \
    ffmpeg \
    libsm6 \
    libxext6
```

### Mac OS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required dependencies
brew install libdmtx
brew install ffmpeg
```

These system dependencies are required for proper functioning of OpenCV and pylibdmtx.

## Installation

You can install GS1Grader using pip:

```bash
pip install gs1grader
```

If you want to install from source:
```bash
# Clone the repo
git clone --recurse-submodules https://github.com/Ceyeborg/GS1Grader.git
cd GS1Grader

# Make the script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

## Usage

Here's a simple example of how to use GS1Grader:

```python
from gs1grader.grader_api import DataMatrixGradeAPI

# Create a grading API instance
grader_api = DataMatrixGradeAPI()

# Grade an image using the modulation grader
grade, explanation = grader_api.grade_datamatrix(
    image_path="path/to/your/datamatrix.png",
    grade_type="modulation",
    explanation_path="."
)

# Print the results
print(f"Grade: {grade}")
if explanation:
    print(f"Explanation: {explanation}")
```

### Available Grading Methods

The library currently supports the following grading methods:
- `modulation`: Evaluates the modulation quality of the Data Matrix
- `symbol_contrast`: Evaluates the symbol contrast quality

### API Reference

#### DataMatrixGradeAPI

The main class for grading Data Matrix codes.

Methods:
- `grade_datamatrix(image_path: str, grade_type: str, explain: bool = False)`:
  - `image_path`: Path to the Data Matrix image file
  - `grade_type`: Type of grading to perform ("modulation" or "symbol_contrast")
  - `explanation_path`: Provide a path to save png of the detailed explanation of the grade (optional)
  - Returns: A tuple of (grade, explanation)

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0) - see the [LICENSE](LICENSE) file for details.

The AGPL-3.0 is a copyleft license that requires anyone who distributes your code or a derivative work to make the source available under the same terms, and also requires you to provide the source code to users who interact with your software as a service.
