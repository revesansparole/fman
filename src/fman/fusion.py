"""Defines a set of functions to compare the content
of two directories in terms of files.

Two main functions:
  - fusion: copy files from source to destination without overwriting
            already existing files
  - compare: internally used to compare attributes of two files
"""

from os import mkdir
from os.path import exists, getsize, join, isdir
from shutil import copy

from . import standard as std


def fusion(src_dir, dst_dir):
    """Fusion the files in src with the content of dst.

    Copy files or directories present exclusively in src into dst.
    In case of files, copy also their associated hash file.

    Args:
      src_dir (str): reference directory path.
      dst_dir (str): directory files will be copied into.

    Returns:
      List of file names present in src_dir and already existing in dst_dir.
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
                # check associated hash
                with open(std.hashname(src_pth), 'rb') as f:
                    src_hash = f.read()

                if exists(std.hashname(dst_pth)):
                    with open(std.hashname(dst_pth), 'rb') as f:
                        dst_hash = f.read()
                else:
                    dst_hash = ""

                if src_hash == dst_hash:
                    # similar files, do nothing
                    # should have check for file integrity before the fusion
                    pass
                else:
                    conflicted.append((src_pth, dst_pth))
            else:
                print("copy: {}".format(src_pth))
                copy(src_pth, dst_pth)
                copy(std.hashname(src_pth), std.hashname(dst_pth))

    return conflicted


def compare(src_pth, dst_pth):
    """Compare attribute of a file both in src and dst.
    """
    # size comparison
    src_size = getsize(src_pth)
    dst_size = getsize(dst_pth)
    if src_size == dst_size:
        sym = '='
    elif src_size > dst_size:
        sym = '>'
    else:
        sym = '<'
    print("{} -> {}".format(src_pth, dst_pth))
    if src_size < 1024 and dst_size < 1024:
        print("          {:d} o {} {:d} o".format(src_size, sym, dst_size))
    elif src_size < 1024 ** 2 and dst_size < 1024 ** 2:
        print("          {:.1f} ko {} {:.1f} ko".format(src_size / 1024, sym, dst_size / 1024))
    else:
        print("          {:.1f} Mo {} {:.1f} Mo".format(src_size / 1024 ** 2, sym, dst_size / 1024 ** 2))
