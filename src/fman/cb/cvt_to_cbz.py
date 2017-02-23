"""Script used to convert files to cbz.
"""

from glob import glob
from os import mkdir, rename
from os.path import basename, exists, join, splitext
# from re import escape
from shutil import move, rmtree
from subprocess import Popen, PIPE
from zipfile import ZipFile, ZIP_DEFLATED, BadZipfile

from fman.cb.editing import make_cbz

tmp_fld = ".tmp_fld"
trash_fld = ".trash"


def cvt(filename):
    fname, ext = splitext(filename)
    ext = ext.lower()

    # test if already zipfile maybe with incorrect extensions
    # try:
    #     f = ZipFile(filename, 'r')
    #     f.close()
    #     rename(filename, "{}.cbz".format(fname))
    # except BadZipfile:
    #     pass

    # clean tmp_fld
    rmtree(tmp_fld)
    mkdir(tmp_fld)

    # extract to tmp_fld
    if ext in (".cbz", ".cbr", ".rar"):
        # cmd = "unar -no-directory -o {} {}".format(tmp_fld, escape(filename) )
        # cmd = "unrar e -o- {} {}".format(escape(filename), tmp_fld)
        cmd = '7z e -o{} "{}"'.format(tmp_fld, filename)
    elif ext == ".pdf":
        # cmd = "pdfimages -all {} {}/page".format(escape(filename), tmp_fld)
        cmd = 'pdfimages "{}" {}/page'.format(filename, tmp_fld)
    else:
        raise UserWarning("unrecognized format for {}".format(filename))

    pip = Popen(cmd,
                shell=True,
                stdout=PIPE,
                stderr=PIPE)
    if pip.wait() != 0:
        print(pip.stderr.read())
        return

    # move file to trash
    move(filename, join(trash_fld, basename(filename)))

    # create archive
    make_cbz(tmp_fld, "{}.cbz".format(fname))


def cvt_files(filenames=None):
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if not exists(tmp_fld):
        mkdir(tmp_fld)

    if not exists(trash_fld):
        mkdir(trash_fld)

    if filenames is None:
        filenames = sorted(glob("*.pdf") + glob("*.cbz") + glob("*.cbr") + glob("*.rar"))

    for filename in filenames:
        print(filename)
        cvt(filename)
