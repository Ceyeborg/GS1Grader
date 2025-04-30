# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "GS1Grader"
copyright = "2025, Ceyeborg GmbH"
author = "Kiran Krishna Tunuguntla"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # For automatically documenting Python modules
    "sphinx.ext.napoleon",  # For Google/NumPy style docstrings
    "sphinx.ext.viewcode",  # For adding links to source code
    "sphinx.ext.intersphinx",  # For linking to other project's documentation
    "sphinx_tabs.tabs",
    "nbsphinx",  # For Jupyter notebook support
]

templates_path = ["_templates"]
exclude_patterns = []

# nbsphinx settings
nbsphinx_execute = "auto"  # Auto-execute notebooks
nbsphinx_allow_errors = True  # Allow errors in notebooks
nbsphinx_timeout = 600  # Increase timeout for notebook execution

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Furo theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#E40EAB",
        "color-brand-content": "#E40EAB",
        "color-toc-foreground--hover": "#E40EAB",
        "color-toc-foreground--active": "#E40EAB",
        "color-announcement-background": "#E40EAB",
        "color-link": "#E40EAB",
        "color-link-underline": "#E40EAB",
        "color-admonition-border--note": "#E40EAB",
        "color-admonition-border--tip": "#E40EAB",
        "color-admonition-border--important": "#E40EAB",
        "color-admonition-border--caution": "#E40EAB",
        "color-admonition-border--warning": "#E40EAB",
    },
    "dark_css_variables": {
        "color-brand-primary": "#E40EAB",
        "color-brand-content": "#E40EAB",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    # "opencv": ("https://docs.opencv.org/4.x/", None),
}
