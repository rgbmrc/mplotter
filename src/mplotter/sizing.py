# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Adjusting the size of matplotlib figures.
"""

from importlib import import_module
from tempfile import NamedTemporaryFile

import numpy as np
import matplotlib as mpl

from mplotter.saving import save_fig

__all__ = ['fig_size', 'get_fig_size', 'set_fig_size']

SUPPORTED_FORMATS = {'eps', 'ps', 'svg'}
"""set[str]: Default supported file formats by :func:`get_fig_size`."""

EXTRAS_FORMATS = {
    'pdf': ('pikepdf', {'pdf'}),
    'raster': ('PIL', {'png', 'jpg', 'jpeg', 'tif', 'tiff'}),
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


def fig_size(width=None, height=None, ratio=None):
    """
    Converts savefig.figsize units to inches.

    For figures with axes of fixed aspect ratio, width and height are
    to be interpreted as maximum values.

    Parameters
    ----------
    width : float, default height / ratio
        Figure width as a fraction of its :rc:`figure.figsize` value.
    height : float, default width * ratio
        Figure height as a fraction of its :rc:`figure.figsize` value.
    ratio : float, default `None`
        Height to width ratio, ignored if both size values are given.

    Returns
    -------
    tuple[float]
        Figure width and height, in inches.
    """
    w, h = mpl.rcParams['figure.figsize']
    if width:
        width *= w
    if height:
        height *= h
    width = width or height / ratio
    height = height or width * ratio
    return width, height


def get_fig_size(fig, **savefig_kw):
    """
    Measures the actual figure size.

    Contrary to the fig.get_size_inches method, returns the show-time
    (rather than draw-time) values. The result depends on file format
    and backend. Supported formats: see SUPPORTED_FORMATS.

    Parameters
    ----------
    fig : :class:`matplotlib.figure.Figure`
        Figure whose size is to be determined.
    **savefig_kw :
        Keyword arguments for :func:`matplotlib.figure.Figure.savefig`.

    Returns
    -------
    tuple[float]
        Actual width and height of the saved figure, in inches.
    """
    dpi = VECTOR_DPI  # when no dpi information available (vector files)
    fmt = savefig_kw.get('format', mpl.rcParams['savefig.format']).lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError('Unsupported format.')
    with NamedTemporaryFile(suffix=f'.{fmt}') as f:
        save_fig(fig, f, close=False, **savefig_kw)
        f.seek(0)
        if fmt == 'pdf':
            import pikepdf
            with pikepdf.open(f) as doc:
                box = list(doc[0].trimbox)
        elif fmt in ('ps', 'eps'):
            for line in f:
                if line.startswith('%%HiResBoundingBox:'):
                    box = line.split()[-4:]
                    break
        elif fmt == 'svg':
            from xml.dom import minidom
            doc = minidom.parse(f)
            doc = doc.documentElement
            size = [
                doc.getAttribute(key).replace('pt', '')
                for key in ('width', 'height')
            ]
        else:
            from PIL import Image
            with Image.open(f, formats=[fmt]) as im:
                size = im.size
            dpi = savefig_kw.get('dpi', mpl.rcParams['savefig.dpi'])
            if dpi == 'figure':
                dpi = fig.dpi
    if not size:
        box = np.asarray(box, dtype=float)
        size = np.diff(box.reshape((2, 2)), axis=0).squeeze()
    return tuple(np.asarray(size, dtype=float) / dpi)


def set_fig_size(fig, width=None, height=None, ratio=None, **savefig_kw):
    """
    Sets the actual figure size, specified in figure.figsize units.

    Contrary to the fig.set_size_inches method, this tries to fix the
    show-time width and height by guessing appropriate draw-time values.
    The result depends on file format and backend.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure whose size has to be adjusted.
    width, height, ratio :
        See docstring for fig_size arguments.
    **savefig_kw :
        Keyword arguments for fig.savefig.
    """
    if width is None and height is None:
        size = fig.get_size_inches()
    else:
        size = fig_size(width, height, ratio)
    size = np.asarray(size)
    draw = [np.zeros(2), size]
    show = [np.zeros(2)]

    def interpolate():
        coeff = np.diff(draw, axis=0) / np.diff(show, axis=0)
        return draw[-1] + (size - show[-1]) * coeff[-1]

    for _ in range(2):
        fig.set_size_inches(draw[-1])
        show.append(get_fig_size(fig, **savefig_kw))
        draw.append(interpolate())

    fig.set_size_inches(draw[-1])
