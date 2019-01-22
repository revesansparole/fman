"""Script to test the integrity of files.

Based on sha512 algorithm to compute the hash code of files
and check it against previously stored hash code.
"""

from . import integrity as igt
from . import standard as std


def _store(pth):
    hash_pth = std.hashname(pth)
    if not hash_pth.exists():
        print(f"storing: {pth}")
        igt.associate_hash(pth)


def store(pth):
    """Associate a hash to a file.

    Store the hash of file content in a companion file in order
    to store it and check later the lack of corruption of the data.

    if the file already has a hashfile associated, does nothing.

    Notes: if pth is a directory, all files in it will be recursively checked

    Args:
        pth (Path): path to store.

    Returns:
        None
    """
    if pth.is_dir():
        for sub_pth in std.walk_files(pth):
            _store(sub_pth)
    else:
        _store(pth)


def _check(pth):
    try:
        valid = "valid:  " if igt.check(pth) else "corrupt:"
        print(f"{valid} {pth}")
    except igt.IOHashError:
        print(f"no valid hash found: {pth}")


def check(pth):
    """Check integrity of files.

    Notes: if pth is a directory, all files in it will be recursively checked

    Args:
        pth (Path): path to check.

    Returns:
        None: result printed on console
    """
    if pth.is_dir():
        for sub_pth in std.walk_files(pth):
            _check(sub_pth)
    else:
        _check(pth)
