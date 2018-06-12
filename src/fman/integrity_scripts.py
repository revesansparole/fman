"""Script to test the integrity of files.

Based on sha512 algorithm to compute the hash code of files
and check it against previously stored hash code.
"""

from os.path import exists

from . import integrity as igt
from . import standard as std


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
        for sub_pth in pth.glob("*"):
            if not std.is_hashname(str(sub_pth)):
                hname = std.hashname(str(sub_pth))
                if not exists(hname):
                    print(f"storing: {sub_pth}")
                    igt.associate_hash(str(sub_pth))
    else:
        hname = std.hashname(str(pth))
        if not exists(hname):
            print(f"storing: {pth}")
            igt.associate_hash(str(pth))


def check(pth):
    """Check integrity of files.

    Notes: if pth is a directory, all files in it will be recursively checked

    Args:
        pth (Path): path to check.

    Returns:
        None: result printed on console
    """
    if pth.is_dir():
        for sub_pth in pth.glob("*"):
            if not std.is_hashname(str(sub_pth)):
                try:
                    valid = "valid:  " if igt.check(str(sub_pth)) else "corrupt:"
                    print(f"{valid} {sub_pth}")
                except igt.IOHashError:
                    print(f"no valid hash found: {sub_pth}")

    else:
        try:
            valid = "valid:  " if igt.check(str(pth)) else "corrupt:"
            print(f"{valid} {pth}")
        except igt.IOHashError:
            print(f"no valid hash found: {pth}")
