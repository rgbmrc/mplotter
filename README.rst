mplotter: matplotlib plotter
============================

Plotting helpers and styles for matplotlib & TeX projects.

Installation
------------

Run :code:`pip install .` in the same folder as this README file.


Extra dependencies
~~~~~~~~~~~~~~~~~~

- `pdf`: enables figure sizing functionality for pdf files;
- `raster`: enables figure sizing functionality for raster files;
- `dev`: for development, see below.

The desired extras can be included by listing them in the install command, e.g. ``pip install .[pdf,raster]``.


Contributing
------------
See `matlotlib's contributing guidelines <https://matplotlib.org/stable/devel/contributing.html#contributing>`_.
To set up for development:

- create a virtual environment via ``python -m venv <location>`` and activate it;
- install the library in editable mode with dev dependencies via ``pip install -e .[dev]``;
- run ``pre-commit install`` to set up the git hook scripts.



Usage
-----

See the `demo script <https://github.com/rgbmrc/mplotter/blob/main/demo.py>`_;
as well as the `documentation <https://mplotter.readthedocs.io/en/latest/reference.html>`_.
