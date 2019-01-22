"""Script used to normalize names of cbz files.
"""

from os import rename
from pathlib import Path

from .book import Book

tmp_fld = Path(".tmp_fld")


def fmt(pth):
    """Normalize name.
    """
    if not tmp_fld.exists():
        tmp_fld.mkdir()

    name = str(Book(pth))
    print("fmt", pth, name)
    if name != pth.name:
        # do rename in two steps to avoid troubles with
        # windows not distinguishing upper from lower
        # letters in file names
        rename(pth, str(tmp_fld / name))
        fmt_pth = pth.parent / name
        if fmt_pth.exists():
            # revert move
            rename(str(tmp_fld / name), pth)
            raise FileExistsError("CBZ file '{}' already exists".format(pth))
        else:
            rename(str(tmp_fld / name), fmt_pth)


def fmt_cbz(pth):
    """Convert files in current directory or whose names have been
    passed on the command line.

    Args:
      pth (Path): Path to format.

    Returns:
      (None)
    """
    if pth.is_dir():
        for sub_pth in pth.glob("*.cbz"):
            fmt(sub_pth)
    else:
        fmt(pth)
