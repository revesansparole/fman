"""Set of functionality to test the integrity of files.

Based on sha512 algorithm to compute the hash code of files
and store it in a companion file. The module provides easy
high level functions to perform common operations.
"""

import hashlib
from os.path import exists

from . import standard as std

__all__ = ["IOHashError", "compute_hash", "associate_hash", "check"]

CHUNK_SIZE = 1000000  # size used to read files chunk by chunk


class IOHashError(IOError):
    """Error used when no associated hash file is found.
    """
    pass


def compute_hash(fname):
    """Compute hash associated with given file.

    Args:
        fname (str): name of the file to read

    Returns:
        A sequence of bytes representing the hash
        of the given file using sha512 algorithm.

    Raises:
        IOError: an error occurred while trying to
          read the file.
    """
    m = hashlib.sha512()

    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            m.update(chunk)

    return m.digest()


def associate_hash(fname):
    """Write hash of a given file to an associated file.

    Args:
        fname (str): name of the file to read

    Returns:
        None

    Raises:
        IOError: an error occurred while trying to
          read the file.
        IOHashError: associated hash file already exists.
    """
    hname = std.hashname(fname)
    if exists(hname):
        raise IOHashError("%s, hashfile already exists" % hname)

    with open(hname, 'wb') as f:
        f.write(compute_hash(fname))


def check(fname):
    """Test whether the given file correspond to its associated hash.

    Args:
        fname (str): name of the file to read

    Returns:
        (bool)

    Raises:
        IOError: an error occurred while trying to
          read the file.
        IOHashError: no associated hash file was found.
    """
    # try to read associated hash file
    hname = std.hashname(fname)
    if not exists(hname):
        raise IOHashError("%s, hashfile not found" % hname)

    with open(hname, 'rb') as f:
        hash_ref = f.read()

    # compute current hash
    hash_cur = compute_hash(fname)

    # comparison
    return hash_cur == hash_ref
