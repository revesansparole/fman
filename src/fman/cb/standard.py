"""Defines standard paths and components for the library.
"""
from pathlib import Path


def book_size(book):
    """Size of file associated to book.

    Args:
        book (Book): book object

    Returns:
        (float): size in [Mo]
    """
    size = book.filename.stat().st_size

    return size / 1024 ** 2


def dirname(cbzname):
    dname = cbzname[0]
    if dname in "0123456789":
        dname = "0"

    return Path(dname)


# extension of files recognized as images
img_ext_needing_cvt = ("jpeg", "jp2", "ppm", "gif")
img_exts = img_ext_needing_cvt + ("jpg", "png")
