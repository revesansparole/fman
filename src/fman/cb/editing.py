"""Regroups functions used to edit cbz files.

examples:
 - make a cbz file from list of image files or the content of a directory
 - remove a page from a cbz file
 - change image format in cbz file
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from PIL import Image

from . import standard as std

__all__ = ["create_cbz", "extract_cover", "make_cbz"]


def create_cbz(outpth, pages):
    """Create a cbz file from a list of image files.

    Args:
        outpth (Path): path to cbz file that will be created
        pages (list of Path): ordered list of path of image files

    Returns:
        None

    Raises:
        FileExistsError: if pth already exists
    """
    if outpth.suffix != ".cbz":
        outpth = outpth.with_suffix(".cbz")

    if outpth.exists():
        raise FileExistsError(f"CBZ file '{outpth}' already exists")

    zf = ZipFile(outpth, 'w', ZIP_DEFLATED)
    for i, pth in enumerate(pages):
        zf.write(pth, f"page{i:04d}{pth.suffix}")

    zf.close()


def make_cbz(dir_pth, pth=None):
    """Create a cbz file with the image content of a directory.

    Args:
        dir_pth (Path): a path to a directory
        pth (Path): name of created cbz file
                     extension will be added if needed
                     if None, use the last component of dname as fname

    Returns:
        None

    Raises:
        FileExistsError: if pth already exists
        FileNotFoundError: if directory is empty
    """
    # format cbz name
    if pth is None:
        pth = Path(dir_pth.name)

    if pth.suffix != ".cbz":
        pth = pth.with_suffix(".cbz")

    if pth.exists():
        raise FileExistsError(f"CBZ file '{pth}' already exists")

    # find image files that need conversion
    to_cvt = set()
    for ext in std.img_ext_needing_cvt:
        to_cvt.update(dir_pth.glob(f"*.{ext}"))
        to_cvt.update(dir_pth.glob(f"*.{ext.upper()}"))

    for img_pth in to_cvt:
        img = Image.open(img_pth)
        if img.mode == 'P':
            img = img.convert("RGB")

        img.save(img_pth.with_suffix(".jpg"))

    # find all jpg/png images in folder
    pages = set()
    for ext in ("jpg", "png"):
        pages.update(dir_pth.glob(f"*.{ext}"))
        pages.update(dir_pth.glob(f"*.{ext.upper()}"))

    if len(pages) == 0:
        msg = f"Directory '{dir_pth}' does not contain any image file"
        raise FileNotFoundError(msg)

    # create cbz
    create_cbz(pth, sorted(pages))


def extract_cover(cbzpth):
    """Extract first page of cbz file.

    Args:
        cbzpth (Path): path to cbz file

    Returns:
        (None): register image with same name than comics
    """
    assert cbzpth.suffix == ".cbz"

    zf = ZipFile(cbzpth, 'r')
    pages = [pth for pth in zf.namelist()
             if Path(pth).suffix.lower()[1:] in std.img_exts]
    pages.sort()

    img_data = zf.read(pages[0])
    img = Image.open(BytesIO(img_data))
    img.save(cbzpth.with_suffix(".jpg"))
