# GS1Grader

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

These system dependencies are required for proper functioning of OpenCV and pylibdmtx.

### Other Linux Distributions
Please install the equivalent packages using your distribution's package manager:
- libdmtx
- ffmpeg
- libsm6
- libxext6

## Installation

You can install GS1Grader using pip:

```bash
pip install gs1grader
```

If you want to install from source:
```bash
git clone https://github.com/yourusername/GS1Grader.git
cd GS1Grader
pip install -e .
```

## Usage

Here's a simple example of how to use GS1Grader:

```python
from core.grader_api import DataMatrixGradeAPI

# Create a grading API instance
grader_api = DataMatrixGradeAPI()

# Grade an image using the modulation grader
grade, explanation = grader_api.grade_datamatrix(
    image_path="path/to/your/datamatrix.png",
    grade_type="modulation",
    explain=True
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
  - `explain`: Whether to provide detailed explanation of the grade (optional)
  - Returns: A tuple of (grade, explanation)

## License

[Add your license information here]
