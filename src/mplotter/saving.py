# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Saving matplotlib figures to file.


"""

from logging import getLogger
from subprocess import run
from pathlib import Path

import matplotlib as mpl

__all__ = ['save_fig']

logger = getLogger(__package__)

SUPPORTED_FORMATS = {'eps', 'ps', 'svg', 'pdf', 'png'}
"""set[str]: Default supported file formats for git revision."""
EXIFTOOL_FORMATS = {'jpg', 'jpeg', 'tif', 'tiff'}
"""set[str]: Optional supported file formats for git revision."""

try:
    run('exiftool', capture_output=True)
except FileNotFoundError:
    exiftool = False
else:
    exiftool = True


def save_fig(fig, dest=None, close=True, **savefig_kw):
    """
    Saves a figure and, optionally, closes it.

    If in a git repository, attempts to store the commit hash of HEAD in
    the "Creator" metadata of the file. Supported file formats are:
    ps, eps, pdf, png, svg; (jpeg and tiff via exiftool). The metadata
    can be retrieved via "exiftool -Creator file" or, for svg files,
    under "/svg/metadata/RDF/Work/creator/Agent/title".

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to be saved.
    dest : str or path-like or file-like, default the figure label
        The destination file, or file name (path without extension).
        If a relative path, :rc:`savefig.directory` is taken as anchor.
        The file format (extension to append to path) can be
        specified via the 'format' savefig_kw and defaults to
        :rc:`savefig.format`.
    close : bool, default True
        Whether to close the figure after saving.
    **savefig_kw :
        Keyword arguments for fig.savefig.

    Returns
    -------
    Path
        The destination path, with extension.
    """
    fmt = savefig_kw.get('format') or mpl.rcParams['savefig.format']
    if not hasattr(dest, 'write'):
        dest = [mpl.rcParams['savefig.directory'], dest or fig.get_label()]
        # last absolute path taken as anchor
        dest = Path(*(Path(p).expanduser() for p in dest))
        dest = dest.with_suffix(f'{dest.suffix}.{fmt}')
        dest.parent.mkdir(parents=True, exist_ok=True)
        path = dest
    else:
        path = Path(dest.name)
        print(path)
    path = path.resolve()

    # git revision in metadata (matplotlib)
    git_rev = run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
    git_rev = git_rev.stdout.strip()
    if git_rev:
        metadata = savefig_kw.setdefault('metadata', {})
        metadata.setdefault('Creator', git_rev)

    fig.savefig(dest, **savefig_kw)
    logger.info(f'Plotted figure {fig.number} to {path}.')

    # git revision in metadata (exiftool)
    if git_rev and exiftool and fmt in EXIFTOOL_FORMATS:
        cmd = ['exiftool', '-overwrite_original', f'-Creator={git_rev}', path]
        run(cmd, check=True, capture_output=True)

    if close:
        import matplotlib.pyplot as plt
        logger.info(f'Closed figure {fig.number}.')
        plt.close(fig)

    return path
