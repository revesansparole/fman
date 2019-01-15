"""Regroups functions used to edit cbz files.

examples:
 - make a cbz file from list of image files or the content of a directory
 - remove a page from a cbz file
 - change image format in cbz file
"""

from glob import escape, glob
from io import BytesIO
from os.path import basename, exists, normpath, splitext
from PIL import Image
from zipfile import ZipFile, ZIP_DEFLATED

from fman.cb import standard as std

__all__ = ["create_cbz", "extract_covert", "make_cbz"]


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

    # find image files that need conversion
    filenames = []
    for ext in std.img_ext_needing_cvt:
        filenames.extend(glob("{}/*.{}".format(escape(dname), ext)))
        filenames.extend(glob("{}/*.{}".format(escape(dname), ext.upper())))

    for img_pth in filenames:
        img = Image.open(img_pth)
        if img.mode == 'P':
            img = img.convert("RGB")

        img.save("{}.jpg".format(splitext(img_pth)[0]))

    # find all jpg/png images in folder
    filenames = []
    for ext in ("jpg", "png"):
        filenames.extend(glob("{}/*.{}".format(escape(dname), ext)))
        # uncomment for linux
        # filenames.extend(glob("{}/*.{}".format(escape(dname), ext.upper())))

    if len(filenames) == 0:
        msg = "Directory '{}' does not contain any image file".format(dname)
        raise FileNotFoundError(msg)

    # create cbz
    create_cbz(fname, sorted(filenames))


def extract_covert(cbzpth):
    """Extract first page of cbz file.

    Args:
        cbzpth (str): path to cbz file

    Returns:
        (None): register image with same name than comix
    """
    cbz_name, ext = splitext(cbzpth)
    assert ext == ".cbz"

    zf = ZipFile(cbzpth, 'r')
    imgfiles = [name for name in zf.namelist() \
                if splitext(name)[1].lower()[1:] in std.img_exts]
    imgfiles.sort()

    img_data = zf.read(imgfiles[0])
    img = Image.open(BytesIO(img_data))
    img = img.convert("RGB")
    img.save("{}.jpg".format(cbz_name))
