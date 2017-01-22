"""Defines standard paths and components for the library.
"""

import os
from os import path

hashext = ".hash"


def hashname(filename):
    """Construct standard name for associated hash file.

    Args:
        filename (str):

    Returns:
        (str)
    """
    return filename + hashext


def is_hashname(filename):
    """Check whether the name corresponds to standard hash file.

    Args:
        filename (str):

    Returns:
        (bool)
    """
    return path.splitext(filename)[1] == hashext


def is_hidden(fpth):
    """Checks whether the path refers to a hidden file.

    Args:
        fpth (str): path to file or directory

    Returns:
        (bool)
    """
    return path.basename(fpth).startswith(".")


def walk(names, hidden_files=False):
    """Walk through all components of names.

    if name is a directory, explore it recursively

    Args:
        names (list of str): list of root paths to explore
        hidden_files (bool): Whether to explore/return hidden files

    Returns:
        (iter of str)
    """
    for name in names:
        if path.isdir(name):
            # recursively explore this directory
            for root, dnames, fnames in os.walk(name):
                # yield directories components
                dnames.sort()
                for i in range(len(dnames) - 1, -1, -1):
                    if hidden_files or not is_hidden(dnames[i]):
                        yield path.join(root, dnames[i])
                    else:
                        # remove hidden directories from future walk
                        del dnames[i]

                # yield files components
                fnames.sort()
                for fname in fnames:
                    if (not is_hashname(fname)) and (hidden_files or not is_hidden(fname)):
                        yield path.join(root, fname)
        else:
            yield name


def walk_files(names, hidden_files=False):
    """Walk through all directories recursively
    and return files in them.

    Args:
        names (list of str): list of root paths to explore
        hidden_files (bool): Whether to explore/return hidden files

    Returns:
        (iter of str)
    """
    for name in walk(names, hidden_files):
        if not path.isdir(name):
            yield name
