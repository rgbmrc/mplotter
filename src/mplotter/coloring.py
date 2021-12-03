# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Coloring figure elements.

Defines a function generating monochromatic colormaps with transparency.
For further colormaps and palettes check out the `palettable library
<https://jiffyclub.github.io/palettable/>`_.
"""

import matplotlib as mpl

__all__ = ['lucid_cmap']


def lucid_cmap(c, name=None, **kwargs):
    """
    Create a colormap from a color, interpolating alpha between 0 and 1.

    Parameters
    ----------
    c : :doc:`color-like <matplotlib:tutorials/colors/colors>`
        The color corresponding to full saturation.
    name : str, default c (if a str) or hex(c)
        Colormap name prefix, '_lucid' is appended.
    **kwargs:
        Keyword arguments passed to
        :class:`~matplotlib.colors.LinearSegmentedColormap`

    Returns
    -------
    :class:`~matplotlib.colors.LinearSegmentedColormap`
        Lucid colormap.
    """
    colors = [mpl.colors.to_rgba(c, alpha=a) for a in (0, 1)]
    name = name or (c if isinstance(c, str) else mpl.colors.to_hex(c))
    name += '_lucid'
    cmap = mpl.colors.LinearSegmentedColormap.from_list(name, colors, **kwargs)
    return cmap
