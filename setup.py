import os
import shutil
import site
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def patch_pylibdmtx():
    """Patch pylibdmtx with our custom files."""
    # Get the site-packages directory
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        # We're in a virtual environment
        site_packages = os.path.join(
            sys.prefix,
            "lib",
            f"python{sys.version_info.major}.{sys.version_info.minor}",
            "site-packages",
        )
    else:
        # We're in the system Python
        site_packages = site.getsitepackages()[0]

    # Path to the installed pylibdmtx package
    pylibdmtx_path = os.path.join(site_packages, "pylibdmtx")

    # Path to our patched files
    patched_dir = os.path.join(os.path.dirname(__file__), "core", "patched")

    # Copy our patched files
    shutil.copy2(
        os.path.join(patched_dir, "pylibdmtx.py"),
        os.path.join(pylibdmtx_path, "pylibdmtx.py"),
    )
    shutil.copy2(
        os.path.join(patched_dir, "wrapper.py"),
        os.path.join(pylibdmtx_path, "wrapper.py"),
    )


class CustomInstall(install):
    def run(self):
        install.run(self)
        patch_pylibdmtx()


class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        patch_pylibdmtx()


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
    url="https://github.com/Ceyeborg/GS1Grader",
    classifiers=[],  # Update with your actual license
    python_requires=">=3.6",
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
)
