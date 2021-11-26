# mplotter: matplotlib plotter

Plotting helpers and styles for matplotlib & TeX projects.

# Installation

Run `pip install .` in the same folder as this README file.


### Extra dependencies:

- pdf: enables figure sizing functionality for pdf files;
- raster: enables figure sizing functionality for raster files;
- dev: for development, see below.

The desired extras can be included by listing them in the install command, e.g. `pip install .[pdf]`.


### Contributing:
See the guidelines in https://matplotlib.org/devdocs/devel/contributing.html.
To set up for development:
- create a virtual environment via `python -m venv <location>` and activate it;
- install the library in editable mode with dev dependencies via `pip install -e .[dev]`;
- run `pre-commit install` to set up the git hook scripts.



# Usage

See the [demo script](demo.py).
