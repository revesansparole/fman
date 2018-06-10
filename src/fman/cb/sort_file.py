"""Script used to sort cbz files in normalized directory architecture
and associate a hash file with them.
"""

from glob import glob
from os import mkdir
from os.path import basename, exists, join
from shutil import move
from sys import argv

from ..integrity import associate_hash
from . import standard as std


def sort(filename):
    """Move file in corresponding directory.
    """
    name = basename(filename)
    dirname = std.dirname(filename)
    tgtname = join(dirname, name)
    if exists(tgtname):
        return None
    else:
        move(filename, tgtname)
        return tgtname


def sort_comix(filenames=None):
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if filenames is None:
        filenames = sorted(glob("*.cbz"))

    for dirname in "0abcdefghijklmnopqrstuvwxyz":
        if not exists(dirname):
            mkdir(dirname)

    for filename in filenames:
        pth = sort(filename)
        if pth is None:
            print("already exists: {}".format(filename))
        else:
            print("moved: {}".format(filename))
            associate_hash(pth)
