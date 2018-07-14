"""Script used to normalize names of cbz files.
"""
from os import rename

from unidecode import unidecode

from . import standard as std


def fmt(pth):
    """Rename file with normalized name.

    Warning: bug when changing the name of a directory

    Args:
      pth (Path): Path to file requiring formatting

    Returns:
      (None)
    """
    name = pth.name.lower()
    name = name.replace("_", " ")
    name = unidecode(name)

    if name != pth.name:
        fmt_pth = pth.parent / name
        if fmt_pth.exists():
            raise FileExistsError("file '{}' already exists".format(fmt_pth))
        else:
            rename(pth, fmt_pth)


def fmt_names(pth):  # TODO what about associated hash file????
    """Convert files in current directory or whose names have been
    passed on the command line.

    Args:
      pth (Path): Path to format.

    Returns:
      (None)
    """
    if pth.is_dir():
        for sub_pth in std.walk_files(pth):
            fmt(sub_pth)
    else:
        fmt(pth)
