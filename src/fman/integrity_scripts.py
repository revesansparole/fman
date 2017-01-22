"""Script to test the integrity of files.

Based on sha512 algorithm to compute the hash code of files
and check it against previously stored hash code.
"""

from os.path import exists

from fman import integrity as igt
from fman import standard as std


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


def check(fnames):
    """Check integrity of files.

    Args:
        fnames (list of str):

    Returns:
        None: result printed on console
    """
    invalids = []
    for fname in std.walk_files(fnames):
        try:
            valid = igt.check(fname)
            print(valid, fname)
            if not valid:
                print("pb with: {}".format(fname))
                invalids.append(fname)
        except igt.IOHashError:
            print(fname, "no valid hash found")

    if len(invalids) > 0:
        print("\n\n\n\nInvalids")
        for name in invalids:
            print(name)
