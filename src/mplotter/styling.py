# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Customizing matploltib style & behaviour.

Consult :doc:`matplotlib:tutorials/introductory/customizing` for an
introduction.
"""

import matplotlib as mpl
import matplotlib.style.core

__all__ = ['use_style']

STYLE_BLACKLIST_EXCLUDES = {'savefig.directory'}


def use_style(style, reset=False):
    """
    Wrapper around :func:`matplotlib.style.use` that allows setting
    :rc:`savefig.directory` via style sheet.

    Parameters
    ----------
    style : str, dict, path-like or list
        A style specification as described in
        :func:`matplotlib.style.use`.
    reset : bool, default False
        Restore the rc params from matplotlib's internal default style
        before applying the specified style.
    """
    # TODO: basic (!) support for dynamic configuration
    mpl.style.core.STYLE_BLACKLIST -= STYLE_BLACKLIST_EXCLUDES
    if reset:
        mpl.rcdefaults()
    mpl.style.core.use(style)
    mpl.style.core.STYLE_BLACKLIST |= STYLE_BLACKLIST_EXCLUDES
