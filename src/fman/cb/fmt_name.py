"""Script used to normalize names of cbz files.
"""

from pathlib import Path

from .book import Book
from ..standard import safe_rename


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
            safe_rename(sub_pth, str(Book(sub_pth)))
    else:
        safe_rename(pth, str(Book(pth)))
