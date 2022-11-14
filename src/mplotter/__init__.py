# Copyright (c) 2021 Marco Rigobello, MIT License
"""
mplotter: matplotlib plotter.

Plotting helpers and styles for matplotlib & TeX projects.
"""

from .saving import *
from .sizing import *
from .styling import *
from . import saving
from . import sizing
from . import styling
from . import annotating
from . import coloring

__all__ = ["save_fig"]

__version__ = "0.1.1"
"""str: Package version."""
