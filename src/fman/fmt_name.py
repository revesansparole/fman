"""Script used to normalize names of cbz files.
"""

from os import rename
from os.path import exists
from unidecode import unidecode

from fman import standard as std


def fmt(filename):
    """Rename file with normalized name.

    Warning: bug when changing the name of a directory

    Args:
      filename (str):

    Returns:
      (None)
    """
    name = filename.lower()
    name = name.replace("_", " ")
    name = unidecode(name)

    if name != filename:
        if exists(name):
            raise FileExistsError("file '{}' already exists".format(name))
        else:
            rename(filename, name)


def fmt_names(fnames):
    """Convert files in current directory or whose names have been
    passed on the command line.

    Args:
      fnames (list of str): set of paths/filenames to explore.

    Returns:
      (None)
    """
    invalids = []
    for fname in std.walk(fnames):
        print(fname)
        fmt(fname)
