import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'GS1Grader'
author = 'Ceyeborg'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_tabs.tabs',     
    'myst_parser'    
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
