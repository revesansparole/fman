"""Script used to sort cbz files in normalized directory architecture
and associate a hash file with them.
"""
from pathlib import Path

from . import standard as std
from ..integrity import associate_hash


def sort(pth):
    """Move file in corresponding directory.

    Args:
      pth (Path): Path to sort

    Returns:
      (Path|None): tgt path or None if it already exists
    """
    pth_tgt = std.dirname(pth.name) / pth.name
    if pth_tgt.exists():
        return None
    else:
        pth.rename(pth_tgt)
        return pth_tgt


def sort_comics(pth):
    """Sort comics in current directory or whose names have been
    passed on the command line.

    Args:
      pth (Path): Path to sort

    Returns:
      (None)
    """
    if pth.is_dir():
        books = sorted(pth.glob("*.cbz"))
    else:
        books = [pth]

    for dpth in (Path(d) for d in "0abcdefghijklmnopqrstuvwxyz"):
        if not dpth.exists():
            dpth.mkdir()

    for pth in books:
        pth_sorted = sort(pth)
        if pth_sorted is None:
            print(f"already exists: {pth}")
        else:
            print(f"moved: {pth}")
            associate_hash(pth_sorted)
