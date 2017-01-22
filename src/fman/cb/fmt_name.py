"""Script used to normalize names of cbz files.
"""

from glob import glob
from os import mkdir, path, rename
from os.path import exists

from fman.cb.book import Book

tmp_fld = ".tmp_fld"


def fmt(filename):
    """Normalize name.
    """
    if not path.exists(tmp_fld):
        mkdir(tmp_fld)

    name = str(Book(filename))
    if name != filename:
        # do rename in two steps to avoid troubles with
        # windows not distinguishing upper from lower
        # letters in file names
        rename(filename, path.join(tmp_fld, filename))
        if exists(name):
            # revert move
            rename(path.join(tmp_fld, filename), filename)
            raise FileExistsError("CBZ file '{}' already exists".format(name))
        else:
            rename(path.join(tmp_fld, filename), name)


def main(filenames=None):
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if filenames is None:
        filenames = sorted(glob("*.cbz"))

    for filename in filenames:
        print(filename)
        fmt(filename)
