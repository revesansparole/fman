"""Script to test the integrity of files.

Based on sha512 algorithm to compute the hash code of files
and check it against previously stored hash code.
"""

from os.path import exists

from . import integrity as igt
from . import standard as std


def store(fnames):
    """Associate a hash file to a given file in order
    to store it and check later the lack of corruption
    of the data.

    if the file already has a hashfile associated, does nothing

    Args:
        fnames (list of str):

    Returns:
        None
    """
    for fname in std.walk_files(fnames):
        hname = std.hashname(fname)
        if not exists(hname):
            print("{}".format(fname))
            igt.associate_hash(fname)


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
                    valid = igt.check(str(sub_pth))
                    print(f"{sub_pth}: {valid}")
                except igt.IOHashError:
                    print(f"{sub_pth}: no valid hash found")

    else:
        try:
            valid = igt.check(str(pth))
            print(f"{pth}: {valid}")
        except igt.IOHashError:
            print(f"{pth}: no valid hash found")
