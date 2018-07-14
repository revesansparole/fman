"""Script used to convert files to cbz.
"""
from itertools import chain
from pathlib import Path
from shutil import rmtree
from subprocess import check_call

from .editing import make_cbz

tmp_fld = Path(".tmp_fld")
trash_fld = Path(".trash")


def cvt(pth):
    print("cbz", pth)

    # clean tmp_fld
    rmtree(tmp_fld)
    tmp_fld.mkdir()

    # extract to tmp_fld
    if pth.suffix in (".cbz", ".cbr", ".rar"):
        cmd = f'7z e -o{tmp_fld} "{pth}"'
    elif pth.suffix == ".pdf":
        cmd = f'pdfimages "{pth}" {tmp_fld}/page'
    else:
        raise UserWarning(f"unrecognized format for {pth}")

    check_call(cmd, shell=True)

    # move file to trash
    pth.rename(trash_fld / pth.name)

    # create archive
    make_cbz(tmp_fld, pth.with_suffix(".cbz"))


def cvt_files(pth):
    """Convert files in current directory or whose names have been
    passed on the command line.

    Args:
      pth (Path): Path to format.

    Returns:
      (None)
    """
    if not tmp_fld.exists():
        tmp_fld.mkdir()

    if not trash_fld.exists():
        trash_fld.mkdir()

    if pth.is_dir():
        for sub_pth in sorted(chain(pth.glob("*.pdf"),
                                    pth.glob("*.cbz"),
                                    pth.glob("*.cbr"),
                                    pth.glob("*.rar"))):
            cvt(sub_pth)
    else:
        cvt(pth)
