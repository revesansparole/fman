"""Script used to normalize names of cbz files.
"""

from glob import glob
from os import rename
from os.path import exists

from fman.cb.book import Book


def fmt(filename):
    """Normalize name.
    """
    name = str(Book(filename))
    if name != filename:
        if exists(name):
            raise FileExistsError("CBZ file '{}' already exists".format(name))
        else:
            rename(filename, name)


def main(filenames=None):
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if filenames is None:
        filenames = sorted(glob("*.cbz"))

    for filename in filenames:
        print(filename)
        fmt(filename)
