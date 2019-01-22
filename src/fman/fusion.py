"""Defines a set of functions to compare the content
of two directories in terms of files.

Two main functions:
  - fusion: copy files from source to destination without overwriting
            already existing files
  - compare: internally used to compare attributes of two files
"""

from shutil import copy

from . import standard as std


def fusion(src_dir, dst_dir):
    """Fusion the content of two directories.

    Copy files or directories present exclusively in src into dst.
    In case of files, copy also their associated hash file.

    Args:
      src_dir (Path): reference directory path.
      dst_dir (Path): directory files will be copied into.

    Returns:
      List of file names present in src_dir and already existing in dst_dir.
    """
    conflicted = []

    for src_pth in std.walk(src_dir):
        # get corresponding dst path
        dst_pth = dst_dir / src_pth.relative_to(src_dir)

        if src_pth.is_dir():  # directory case
            if not dst_pth.exists():
                print(f"create: {dst_pth}")
                dst_pth.mkdir()
        else:  # file case
            if not std.hashname(src_pth).exists():
                raise UserWarning(f"file does not have associated hash:\n{src_pth}")

            if dst_pth.exists():
                # check associated hash
                with open(std.hashname(src_pth), 'rb') as f:
                    src_hash = f.read()

                try:
                    with open(std.hashname(dst_pth), 'rb') as f:
                        dst_hash = f.read()
                except FileNotFoundError:
                    dst_hash = ""

                if src_hash == dst_hash:
                    # similar files, do nothing
                    # should have check for file integrity before the fusion
                    pass
                else:
                    conflicted.append((src_pth, dst_pth))
            else:
                print(f"copy: {src_pth}")
                copy(src_pth, dst_pth)
                copy(std.hashname(src_pth), std.hashname(dst_pth))

    return conflicted


def compare(src_pth, dst_pth):
    """Compare attribute of a file both in src and dst.
    """
    # size comparison
    src_size = src_pth.stat().st_size
    dst_size = dst_pth.stat().st_size
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
