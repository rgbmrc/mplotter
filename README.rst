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

The desired extras can be included by listing them in the install
command, e.g. ``pip install .[pdf,raster]``.



Usage
-----

See the `demo script
<https://github.com/rgbmrc/mplotter/blob/main/demo.py>`_;
as well as the `reference documentation
<https://mplotter.readthedocs.io/en/latest/reference.html>`_.



Contributing
------------

The project is hosted at `<https://github.com/rgbmrc/mplotter>`_.

Use the `issue tracker <https://github.com/rgbmrc/mplotter/issues>`_
to submit bug reports or feature requests. To contribute the codebase,
create a fork of the project repository on github and work on a new
brach. When you're done open a pull request.
See e.g. `matlotlib's contributing guidelines
<https://matplotlib.org/stable/devel/contributing.html#contributing>`_
for an overview of some best practices.

To set up for development:

- clone the github repository via
- create a virtual environment via ``python -m venv <location>``
  and activate it;
- install the library in editable mode with dev dependencies via
  ``pip install -e .[dev]``;
- run ``pre-commit install`` to set up the git hook scripts.
