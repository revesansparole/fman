"""Defines standard paths and components for the library.
"""

from os import rename
from pathlib import Path

tmp_fld = Path(".tmp_fld")
hashext = ".hash"


def hashname(pth):
    """Construct standard name for associated hash file.

    Args:
        pth (Path):

    Returns:
        (pth)
    """
    return pth.parent / (pth.name + hashext)


def is_hashname(pth):
    """Check whether the name corresponds to standard hash file.

    Args:
        pth (Path):

    Returns:
        (bool)
    """
    return pth.suffix == hashext


def is_hidden(pth):
    """Checks whether the path refers to a hidden file.

    Args:
        pth (Path): path to file or directory

    Returns:
        (bool)
    """
    return pth.name.startswith(".")


def safe_rename(pth, name):
    """Normalize name.
    """
    if not tmp_fld.exists():
        tmp_fld.mkdir()

    print("rename", pth, name)
    if name != pth.name:
        # do rename in two steps to avoid troubles with
        # windows not distinguishing upper from lower
        # letters in file names
        rename(pth, str(tmp_fld / name))
        fmt_pth = pth.parent / name
        if fmt_pth.exists():
            # revert move
            rename(str(tmp_fld / name), pth)
            raise FileExistsError("CBZ file '{}' already exists".format(pth))
        else:
            rename(str(tmp_fld / name), fmt_pth)


def walk(root, hidden_files=False):
    """Walk recursively through all paths in root.

    Args:
        root (Path): root path to explore
        hidden_files (bool): Whether to explore/return hidden files

    Returns:
        (iter of str)
    """
    for child in root.iterdir():
        if hidden_files or not is_hidden(child):
            if not is_hashname(child):
                yield child

            if child.is_dir():
                for sub_child in walk(child, hidden_files):
                    yield sub_child


def walk_files(root, hidden_files=False):
    """Walk recursively through all files only in root.

    Args:
        root (Path): root path to explore
        hidden_files (bool): Whether to explore/return hidden files

    Returns:
        (iter of str)
    """
    for pth in walk(root, hidden_files):
        if pth.is_file():
            yield pth
