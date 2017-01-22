"""Regroups functions used to edit cbz files.

examples:
 - make a cbz file from list of image files or the content of a directory
 - remove a page from a cbz file
 - change image format in cbz file
"""

from glob import escape, glob
from os.path import basename, exists, normpath, splitext
from zipfile import ZipFile, ZIP_DEFLATED

from fman.bd import standard as std

__all__ = ["create_cbz", "make_cbz"]


def create_cbz(fname, images):
    """Create a cbz file from a list of image files.

    Args:
        fname (str): name of created cbz file
                     extension will be added if needed
        images (list of str): ordered list of path of image files

    Returns:
        None

    Raises:
        FileExistsError: if fname is already existing
    """
    if not fname.endswith(".cbz"):
        fname += ".cbz"

    if exists(fname):
        raise FileExistsError("CBZ file '{}' already exists".format(fname))

    zf = ZipFile(fname, 'w', ZIP_DEFLATED)
    for i, name in enumerate(images):
        zf.write(name, "page{:04d}{}".format(i, splitext(name)[1]))

    zf.close()


def make_cbz(dname, fname=None):
    """Create a cbz file with the image content of a directory.

    Args:
        dname (str): a path to a directory
        fname (str): name of created cbz file
                     extension will be added if needed
                     if None, use the last component of dname as fname

    Returns:
        None

    Raises:
        FileExistsError: if fname is already existing
        FileNotFoundError: if directory is empty
    """
    dname = normpath(dname)

    # format cbz name
    if fname is None:
        fname = basename(dname)

    if not fname.endswith(".cbz"):
        fname += ".cbz"

    if exists(fname):
        raise FileExistsError("CBZ file '{}' already exists".format(fname))

    # find image files
    filenames = []
    for ext in std.img_exts:
        filenames.extend(glob("{}/*.{}".format(escape(dname), ext)))
        filenames.extend(glob("{}/*.{}".format(escape(dname), ext.upper())))

    if len(filenames) == 0:
        msg = "Directory '{}' does not contain any image file".format(dname)
        raise FileNotFoundError(msg)

    # create cbz
    create_cbz(fname, sorted(filenames))
