# Copyright (c) 2021 Marco Rigobello, MIT License
"""
Saving matplotlib figures to file.

`Reproducibility` is a key requirement for publishing scientific work.
As far as illustrations are concerned, reproducibility can be achieved
using a `VCS <https://en.wikipedia.org/wiki/Version_control>`_ to track
changes to the plotting code. When the CWD is in a `git <https://git-
scm.com/>`_ repository, the function :func:`save_fig` provided by this
module stores the commit hash of HEAD in the "Creator" metadata of the
saved figure. Some file formats are supported only through `exiftool
<http://exiftool.sourceforge.net/>`_ (see :data:`SUPPORTED_FORMATS` and
:data:`EXIFTOOL_FORMATS`). The metadata can be retrieved e.g. via
``exiftool -Creator <filename(s)>`` or, for svg files, under the tag
``/svg/metadata/RDF/Work/creator/Agent/title``.
"""

from contextlib import contextmanager
from logging import getLogger
from subprocess import run
from pathlib import Path

import matplotlib as mpl

__all__ = ["fig_dir", "save_fig"]

logger = getLogger(__package__)

SUPPORTED_FORMATS = {"eps", "ps", "svg", "pdf", "png"}
"""set[str]: Default supported file formats for git revision."""
EXIFTOOL_FORMATS = {"jpg", "jpeg", "tif", "tiff"}
"""set[str]: Exiftool supported file formats for git revision."""

try:
    run("exiftool", capture_output=True)
except FileNotFoundError:
    exiftool = False
else:
    exiftool = True


def _resolve_path(path=None):
    """
    Resolves an absolute or relative path.

    User constructs are expanded and :rc:`savefig.directory` is used as anchor.

    Parameters
    ----------
    path : str or path-like, default '.'
        The path to resolve, absolute or relative.

    Returns
    -------
    :class:`pathlib.Path`
        The resolved path.
    """
    segments = (mpl.rcParams["savefig.directory"], path or ".")
    return Path(*(Path(p).expanduser() for p in segments))


def get_fig_label(fig):
    """Returns a figure's label or, as a fallback, its number."""
    return fig.get_label() or fig.number


@contextmanager
def fig_dir(dest):
    """
    A context manager for temporarily changing the plotting directory.

    Sets :rc:`savefig.directory` via :func:`~matplotlib.rc_context`.

    Parameters
    ----------
    dest : str or path-like
        The new destination directory. If a relative path,
        :rc:`savefig.directory` is taken as anchor.
    """
    with mpl.rc_context({"savefig.directory": str(_resolve_path(dest))}):
        yield


def save_fig(fig, dest=None, close=True, **savefig_kw):
    """
    Saves a figure and, optionally, closes it.

    The way in which the destination path is specified differs from the
    one used by :meth:`~matplotlib.figure.Figure.savefig`. Moreover, if
    the CWD is in a git repository, attempts to store the commit hash of
    HEAD in the "Creator" metadata of the file. Supported file formats:
    ps, eps, pdf, png, svg; (jpeg and tiff via exiftool). Monitoring
    information is emitted through python's :mod:`logging` module.

    Parameters
    ----------
    fig : :class:`~matplotlib.figure.Figure`
        The figure to be saved.
    dest : str or path-like or file-like, default the figure label
        The destination file, or file name (path without extension).
        If a relative path, :rc:`savefig.directory` is taken as anchor.
        The file format (extension to append to path) can be
        specified via ``savefig_kw['format']`` and defaults to
        :rc:`savefig.format`.
    close : bool, default True
        Whether to call :func:`matplotlib.pyplot.close` on the figure
        after saving.
    **savefig_kw :
        Keyword arguments for :meth:`~matplotlib.figure.Figure.savefig`.

    Returns
    -------
    :class:`pathlib.Path`
        The destination path, with extension.
    """
    fmt = savefig_kw.get("format") or mpl.rcParams["savefig.format"]
    try:
        dest = Path(dest or fig.get_label())
    except TypeError:
        # file-like dest, path stored for logging reasons
        path = Path(dest.name)
    else:
        dest = _resolve_path(dest).with_suffix(f"{dest.suffix}.{fmt}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        path = dest
    path = path.resolve()

    # git revision in metadata (matplotlib)
    git_rev = run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    git_rev = git_rev.stdout.strip()
    if git_rev:
        metadata = savefig_kw.setdefault("metadata", {})
        metadata.setdefault("Creator", git_rev)

    fig.savefig(dest, **savefig_kw)
    logger.info(f"Plotted figure {get_fig_label(fig)} to {path}.")

    # git revision in metadata (exiftool)
    # TODO: maybe replacable with exif pil_kwargs?
    if git_rev and exiftool and fmt in EXIFTOOL_FORMATS:
        cmd = ["exiftool", "-overwrite_original", f"-Creator={git_rev}", path]
        run(cmd, check=True, capture_output=True)

    if close:
        import matplotlib.pyplot as plt

        logger.debug(f"Closed figure {get_fig_label(fig)}.")
        plt.close(fig)

    return path
