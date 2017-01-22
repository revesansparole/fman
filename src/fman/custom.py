"""Custom function
"""

from os import getcwd, mkdir
from os.path import exists, getsize, join, isdir
from shutil import copy
from sys import argv

import standard as std


def custom(src_dir, dst_dir):
    """copy hashfiles from src to dst
    """
    nb = len(src_dir) + 1
    conflicted = []

    for src_pth in std.walk([src_dir]):
        # get corresponding dst path
        dst_pth = join(dst_dir, src_pth[nb:])

        if isdir(src_pth):  # directory case
            if exists(dst_pth):
                # do nothing
                pass
            else:
                print("create: {}".format(dst_pth))
                mkdir(dst_pth)
        else:  # file case
            if not exists(std.hashname(src_pth)):
                msg = "file does not have asociated hash:\n{}".format(src_pth)
                raise UserWarning(msg)

            if exists(dst_pth):
                if not exists(std.hashname(dst_pth)):
                    copy(std.hashname(src_pth), std.hashname(dst_pth))
            else:
                print("copy: {}".format(src_pth))
                copy(src_pth, dst_pth)
                copy(std.hashname(src_pth), std.hashname(dst_pth))

    return conflicted


def main():
    """Perform fusion based on command line arguments.
    """
    if len(argv) == 1:
        raise UserWarning("I need at least a destination directory")
    elif len(argv) == 2:
        src_dir = getcwd()
        dst_dir = argv[1]
    else:
        src_dir, dst_dir = argv[1:3]

    conflicts = custom(src_dir, dst_dir)

    for names in conflicts:
        print(names)
