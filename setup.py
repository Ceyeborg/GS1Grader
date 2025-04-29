import os
import shutil
import site
import sys

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def patch_pylibdmtx():
    """Patch pylibdmtx with our custom files."""
    try:
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
        print(f"Patching pylibdmtx at: {pylibdmtx_path}", flush=True)

        # Path to our patched files
        patched_dir = os.path.join(
            os.path.dirname(__file__), "core", "patched"
        )
        print(f"Using patched files from: {patched_dir}", flush=True)

        # Copy our patched files
        files_to_patch = ["pylibdmtx.py", "wrapper.py", "dmtx_library.py"]
        for file in files_to_patch:
            src = os.path.join(patched_dir, file)
            dst = os.path.join(pylibdmtx_path, file)
            print(f"Patching {file}...")
            shutil.copy2(src, dst)
            print(f" Successfully patched {file}", flush=True)

        print("Patching completed successfully!", flush=True)
        return True
    except Exception as e:
        print(f"Error during patching: {repr(e)}")
        return False


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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: AGPL-3.0",
        "Operating System :: OS Independent", 
    ],
    python_requires=">=3.6",
    cmdclass={
        "install": CustomInstall,
        "develop": CustomDevelop,
    },
)
