# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Adjusting the size of matplotlib figures.

When preparing complex documents consisting of text and visual elements,
it is often crucial to:

1.  Fit a figure in a specific region of the document.

2.  Avoid any rescaling of the figure upon inclusion, so that its fixed
    size components (e.g. text elements) are preserved.

To this aim,

1.  It might be convenient to use the size of other layout elements of
    the document (line width, slide height, etc.) as length units.

2.  It is necessary to ensure that a figure is sized accurately.

This module provides helper functions to achieve both these goals.
Precisely,

1.  The function :func:`fig_size` allows to use the values (in inches)
    in :rc:`figure.figsize` as custom width and height units, converting
    a length specified in these units to its value in inches (standard
    matplotlib's unit). The latter can then be used as input elsewhere.

    When typesetting a TeX document, the size (in pt) of many layout
    elements can be assessed including the `command
    <https://www.tug.org/utilities/plain/cseq.html#showthe-rp>`_
    ``\showthe\<somelength>`` and inspecting the compiler log;
    ``<somelength>`` is the name of the layout element (for a list of
    common possibilities see `this table
    <https://www.overleaf.com/learn/latex/Lengths_in_LaTeX#Lengths>`_).
    To convert the output to inches, simply divide by ``72.27``.


2.  The function :func:`get_fig_size` retrives the save-time size of a
    figure (for a specific backend). Calling this function iteratively,
    :func:`set_fig_size` attemps to enforce a given save-time size for
    a figure, adjusting its draw-time size.

    Built-in support is available only for a handful of vector formats,
    listed in :data:`SUPPORTED_FORMATS`. For other file formats, extra
    dependencies are required (see :data:`EXTRAS_FORMATS`).
"""

from importlib import import_module
from tempfile import NamedTemporaryFile

import numpy as np
import matplotlib as mpl

from mplotter.saving import save_fig

__all__ = ["fig_size", "get_fig_size", "set_fig_size"]

SUPPORTED_FORMATS = {"eps", "ps", "svg"}
"""set[str]: Supported file formats by :func:`get_fig_size`."""

EXTRAS_FORMATS = {
    "pdf": ("pikepdf", {"pdf"}),
    "raster": ("PIL", {"png", "jpg", "jpeg", "tif", "tiff"}),
}
"""set[str]: Optional supported file formats by :func:`get_fig_size`."""

for pkg, fmts in EXTRAS_FORMATS.values():
    try:
        import_module(pkg)
    except ModuleNotFoundError:
        pass
    else:
        SUPPORTED_FORMATS |= fmts

VECTOR_DPI = 72.0


def fig_size(width=None, height=None, ratio=0.618):
    """
    Converts :rc:`savefig.figsize` units to inches.

    For figures with axes of fixed aspect ratio, width and height are
    to be interpreted as maximum values.

    Parameters
    ----------
    width : float, default :obj:`height / ratio`
        Figure width as a fraction of its :rc:`figure.figsize` value.
    height : float, default :obj:`width * ratio`
        Figure height as a fraction of its :rc:`figure.figsize` value.
    ratio : float, default golden ratio ``0.618``
        Height to width ratio, ignored if both size values are given.

    Returns
    -------
    tuple[float]
        Figure width and height, in inches.
    """
    w, h = mpl.rcParams["figure.figsize"]
    if width:
        width *= w
    if height:
        height *= h
    width = width or height / ratio
    height = height or width * ratio
    return width, height


def get_fig_size(fig, **savefig_kw):
    """
    Measures the actual saved figure size.

    Contrary to the fig.get_size_inches method, returns the save-time
    (rather than draw-time) values. The result depends on the backend.
    Supported formats: see :data:`SUPPORTED_FORMATS`.

    Parameters
    ----------
    fig : :class:`~matplotlib.figure.Figure`
        Figure whose size is to be determined.
    **savefig_kw :
        Keyword arguments for :meth:`~matplotlib.figure.Figure.savefig`.

    Returns
    -------
    tuple[float]
        Actual width and height of the saved figure, in inches.
    """
    dpi = VECTOR_DPI  # when no dpi information available (vector files)
    fmt = savefig_kw.get("format", mpl.rcParams["savefig.format"]).lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported format.")
    with NamedTemporaryFile(suffix=f".{fmt}") as f:
        save_fig(fig, f, close=False, **savefig_kw)
        f.seek(0)
        size = None
        if fmt == "pdf":
            import pikepdf

            with pikepdf.open(f) as doc:
                box = list(doc.pages[0].trimbox)
        elif fmt in ("ps", "eps"):
            for line in f:
                if line.startswith("%%HiResBoundingBox:"):
                    box = line.split()[-4:]
                    break
        elif fmt == "svg":
            from xml.dom import minidom

            doc = minidom.parse(f).documentElement
            size = [
                doc.getAttribute(key).replace("pt", "") for key in ("width", "height")
            ]
        else:
            from PIL import Image

            with Image.open(f, formats=[fmt]) as im:
                size = im.size
            dpi = savefig_kw.get("dpi", mpl.rcParams["savefig.dpi"])
            if dpi == "figure":
                dpi = fig.dpi
    if not size:
        box = np.asarray(box, dtype=float)
        size = np.diff(box.reshape((2, 2)), axis=0).squeeze()
    return tuple(np.asarray(size, dtype=float) / dpi)


def set_fig_size(fig, size=None, **savefig_kw):
    """
    Sets the actual saved figure size.

    Contrary to the :meth:`~matplotlib.figure.Figure.set_size_inches`,
    this tries to fix the save-time width and height by guessing
    appropriate draw-time values. The result depends on the backend.

    Parameters
    ----------
    fig : :class:`~matplotlib.figure.Figure`
        Figure whose size has to be adjusted.
    size : float, default ``fig.get_size_inches()``
        Desired save-time figure size, in inches.
    **savefig_kw :
        Keyword arguments for :meth:`~matplotlib.figure.Figure.savefig`.

    Returns
    -------
    tuple[float]
        Draw-time width and height of the figure, in inches.
    """
    size = np.asarray(size or fig.get_size_inches())
    draw = [np.zeros(2), size]
    show = [np.zeros(2)]

    def interpolate():
        coeff = np.diff(draw, axis=0) / np.diff(show, axis=0)
        return draw[-1] + (size - show[-1]) * coeff[-1]

    for _ in range(2):
        fig.set_size_inches(draw[-1])
        show.append(get_fig_size(fig, **savefig_kw))
        if np.allclose(show[-1], size):
            break
        draw.append(interpolate())

    fig.set_size_inches(draw[-1])
    return draw[-1]
