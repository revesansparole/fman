"""Set of functionality to test the integrity of files.

Based on sha512 algorithm to compute the hash code of files
and store it in a companion file. The module provides easy
high level functions to perform common operations.
"""

import hashlib

from . import standard as std

__all__ = ["IOHashError", "compute_hash", "associate_hash", "check"]

CHUNK_SIZE = 1000000  # size used to read files chunk by chunk


class IOHashError(IOError):
    """Error used when no associated hash file is found.
    """
    pass


def compute_hash(pth):
    """Compute hash associated with given file.

    Args:
        pth (Path): path to file to read

    Returns:
        A sequence of bytes representing the hash
        of the given file using sha512 algorithm.

    Raises:
        IOError: an error occurred while trying to
          read the file.
    """
    m = hashlib.sha512()

    with open(pth, 'rb') as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            m.update(chunk)

    return m.digest()


def associate_hash(pth):
    """Write hash of a given file to an associated file.

    Args:
        pth (Path): path to file to read

    Returns:
        None

    Raises:
        IOError: an error occurred while trying to
          read the file.
        IOHashError: associated hash file already exists.
    """
    hash_pth = std.hashname(pth)
    if hash_pth.exists():
        raise IOHashError(f"{hash_pth}, hashfile already exists")

    with open(hash_pth, 'wb') as f:
        f.write(compute_hash(pth))


def check(pth):
    """Test whether the given file correspond to its associated hash.

    Args:
        pth (Path): path to file to read

    Returns:
        (bool)

    Raises:
        IOError: an error occurred while trying to
          read the file.
        IOHashError: no associated hash file was found.
    """
    # read previously stored hash
    try:
        with open(std.hashname(pth), 'rb') as f:
            hash_ref = f.read()
    except FileNotFoundError:
        raise IOHashError(f"{pth}, hashfile not found")

    # compute current
    hash_cur = compute_hash(pth)

    # return comparison of both
    return hash_cur == hash_ref
