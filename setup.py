from setuptools import find_packages, setup

setup(
    name="gs1grader",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib==3.8.2",
        "pylibdmtx==0.1.10",
        "numpy==1.26.2",
        "opencv-python==4.8.1.78",
    ],
    author="Ceyeb.org",
    author_email="info@ceyeb.org",
    description="A library for grading Data Matrix codes using \
        GS1 quality metrics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/GS1Grader",
    classifiers=[],  # Update with your actual license
    python_requires=">=3.6",
)
