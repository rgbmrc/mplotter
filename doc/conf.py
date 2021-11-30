# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('.'))

import mplotter

# -- Project information -----------------------------------------------------

project = 'mplotter'
copyright = '2021, Marco Rigobello'
author = 'Marco Rigobello'

# The short X.Y version
version = mplotter.__version__

# The full version, including alpha/beta/rc tags
release = mplotter.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.graphviz',
    'sphinx_rtd_theme',
    'sphinx.ext.viewcode',
    'extensions.custom_roles',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'templates', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['static']
html_css_files = [
    'custom.css',
]
html_theme_options = {
    'collapse_navigation': False,  # 'style_external_links': True,
}

# -- sphinx.ext.autodoc ---------------------------------------------------

autodoc_default_options = {'ignore-module-all': True}
autodoc_member_order = 'bysource'

# -- sphinx.ext.autosummary ---------------------------------------------------

# some options are included in the templates under
# sphinx_templates/autosummary/class.rst
# for example :inherited-members: and :show-inheritance:
autosummary_generate = True

# -- sphinx.ext.intersphinx -----------------------------------------------
# cross links to other sphinx documentations
# this makes  e.g. :class:`numpy.ndarray` work
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
}
add_module_names = False

# -- sphinx.ext.inheritance_diagram ---------------------------------------

inheritance_graph_attrs = {
    'rankdir': "TB",  # top-to-bottom
    'fontsize': 12,
    'ratio': 'compress',
}
graphviz_output_format = 'svg'
