"""Script used to normalize names of cbz files.
"""

from glob import glob
from os import rename
from os.path import exists
from sys import argv

from fman.bd.book import Book


def fmt(filename):
    """Normalize name.
    """
    name = str(Book(filename))
    if name != filename:
        if exists(name):
            raise FileExistsError("CBZ file '{}' already exists".format(name))
        else:
            rename(filename, name)


def main():
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if len(argv) == 1:
        filenames = sorted(glob("*.cbz"))
    else:
        filenames = argv[1:]

    for filename in filenames:
        print(filename)
        fmt(filename)


if __name__ == "__main__":
    main()
