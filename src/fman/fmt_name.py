"""Script used to normalize names of cbz files.
"""

from os import rename
from os.path import exists
from sys import argv
from unidecode import unidecode

import standard as std


def fmt(filename):
    """Normalize name.

    ..warning: bug when changing the name of a directory
    """
    name = filename.lower()
    name = name.replace("_", " ")
    name = unidecode(name)

    if name != filename:
        if exists(name):
            raise FileExistsError("file '{}' already exists".format(name))
        else:
            rename(filename, name)


def main():
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if len(argv) == 1:
        fnames = ["."]
    else:
        fnames = argv[1:]

    invalids = []
    for fname in std.walk(fnames):
        print(fname)
        fmt(fname)


if __name__ == "__main__":
    main()
