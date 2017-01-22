"""Script used to convert files to cbz.
"""

from glob import glob
from os import mkdir, rename
from os.path import basename, exists, join, splitext
from re import escape
from shutil import move, rmtree
from subprocess import Popen, PIPE
from sys import argv
from zipfile import ZipFile, ZIP_DEFLATED, BadZipfile

from fman.bd.editing import make_cbz

tmp_fld = ".tmp_fld"
trash_fld = ".trash"


def cvt(filename):
    fname, ext = splitext(filename)

    # test if already zipfile maybe with incorrect extensions
    try:
        f = ZipFile(filename, 'r')
        f.close()
        rename(filename, "{}.cbz".format(fname))
        return
    except BadZipfile:
        pass

    # clean tmp_fld
    rmtree(tmp_fld)
    mkdir(tmp_fld)

    # extract to tmp_fld
    if ext in (".cbr", ".rar"):
        # cmd = "unar -no-directory -o {} {}".format(tmp_fld, escape(filename) )
        cmd = "unrar e -o- {} {}".format(escape(filename), tmp_fld)
    elif ext == ".pdf":
        cmd = "pdfimages -all {} {}/page".format(escape(filename), tmp_fld)
    else:
        raise UserWarning("unrecognized format for {}".format(filename))

    pip = Popen(cmd,
                shell=True,
                stdout=PIPE,
                stderr=PIPE)
    pip.wait()

    # move file to trash
    move(filename, join(trash_fld, basename(filename)))

    # create archive
    make_cbz(tmp_fld, "{}.cbz".format(fname))


def main():
    """Convert files in current directory or whose names have been
    passed on the command line.
    """
    if not exists(tmp_fld):
        mkdir(tmp_fld)

    if not exists(trash_fld):
        mkdir(trash_fld)

    if len(argv) == 1:
        filenames = sorted(glob("*.pdf") + glob("*.cbr") + glob("*.rar"))
    else:
        filenames = argv[1:]

    for filename in filenames:
        print(filename)
        cvt(filename)


if __name__ == "__main__":
    main()
