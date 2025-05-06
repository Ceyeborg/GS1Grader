import os
import shutil

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def copy_custom_pylibdmtx():
    """
    Copy patched pylibdmtx files from the submodule into the
    local package directory.
    """
    try:
        # Source directory in submodule
        submodule_src = os.path.join(
            os.path.dirname(__file__), "external", "pylibdmtx", "pylibdmtx"
        )
        # Destination directory in the gs1grader package
        target_dst = os.path.join(
            os.path.dirname(__file__), "src", "gs1grader", "pylibdmtx"
        )

        print(
            f"Copying pylibdmtx files from:\n  \
            {submodule_src}\nto:\n  {target_dst}\n",
            flush=True,
        )

        os.makedirs(target_dst, exist_ok=True)

        files_to_copy = [
            "pylibdmtx.py",
            "wrapper.py",
            "dmtx_library.py",
            "pylibdmtx_error.py",
        ]
        for file in files_to_copy:
            src = os.path.join(submodule_src, file)
            dst = os.path.join(target_dst, file)
            shutil.copy2(src, dst)
            print(f"  Copied {file} ✔", flush=True)

        print("Custom pylibdmtx files copied successfully.\n", flush=True)
        return True
    except Exception as e:
        print(f"Error copying custom pylibdmtx files: {repr(e)}")
        return False


class CustomInstall(install):
    def run(self):
        install.run(self)
        copy_custom_pylibdmtx()


class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        copy_custom_pylibdmtx()


setup(
    name="gs1grader",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "matplotlib==3.8.2",
        "pylibdmtx==0.1.10",
        "numpy==1.26.2",
        "opencv-python==4.8.1.78",
    ],
    author="Ceyeb.org",
    author_email="info@ceyeb.org",
    description="A library for grading Data Matrix codes using"
    "GS1 quality metrics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ceyeborg/GS1Grader",
    classifiers=[],
    python_requires=">=3.6",
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
)
