# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Customizing matploltib style & behaviour.

see https://matplotlib.org/stable/tutorials/introductory/customizing.html

"""

import matplotlib as mpl
import matplotlib.style.core

__all__ = ['use_style']

STYLE_BLACKLIST_EXCLUDES = {'savefig.directory'}


def use_style(style, reset=False):
    """
    Wrapper around matplotlib.style.use that allows setting
    :rc:`savefig.directory` via style sheet.

    Parameters
    ----------
    style : str, dict, Path or list
        A style specification as described in matplotlib.style.use.
    reset : bool, default False
        Restore the rc params from matplotlib's internal default style.
    """
    # TODO: basic (!) support for dynamic configuration
    mpl.style.core.STYLE_BLACKLIST -= STYLE_BLACKLIST_EXCLUDES
    if reset:
        mpl.rcdefaults()
    mpl.style.core.use(style)
    mpl.style.core.STYLE_BLACKLIST |= STYLE_BLACKLIST_EXCLUDES
