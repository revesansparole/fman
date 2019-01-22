from argparse import ArgumentParser
from pathlib import Path

from . import logging_tools
from .cb.cvt_to_cbz import cvt_files
from .cb.editing import extract_cover
from .cb.fmt_name import fmt_cbz
from .cb.sort_file import sort_comics
from .cb.txt_translator import main as txt_translator
from .fmt_name import fmt_names
from .fusion import compare, fusion
from .integrity_scripts import check, store


def action_check(**kwds):
    """Check whether files are still valid.
    """
    pth = Path(kwds['pth'])
    check(pth)


def action_fmt_names(**kwds):
    """Rename files with normalized names.
    """
    pth = Path(kwds['pth'])
    fmt_names(pth)


def action_fusion(**kwds):
    """Attempt to fusion the content of two directories.
    """
    src = Path(kwds['src'])
    dst = Path(kwds['dst'])

    conflicts = fusion(src, dst)

    for names in conflicts:
        compare(*names)


def action_store(**kwds):
    """Associate hash to files.
    """
    pth = Path(kwds['pth'])
    store(pth)


def action_cb_fmt(**kwds):
    """Format cbz file names.
    """
    pth = Path(kwds['pth'])
    fmt_cbz(pth)


def action_cb_cvt(**kwds):
    """Convert file to cbz.
    """
    pth = Path(kwds['pth'])
    cvt_files(pth)


def action_cb_sort(**kwds):
    """Sort cbz files into dirs.
    """
    pth = Path(kwds['pth'])
    sort_comics(pth)


def action_cb_cover(**kwds):
    """Extract cover of cbz files in current working directory.
    """
    pth = Path(kwds['pth'])
    if pth.is_dir():
        for sub_pth in pth.glob("*.cbz"):
            extract_cover(sub_pth)
    else:
        extract_cover(pth)


def action_txt_translate(**kwds):
    """List book collection into txt file
    """
    txt_translator()


def main():
    """Run CLI evaluation"""
    action = dict(check=action_check,
                  fmt=action_fmt_names,
                  fusion=action_fusion,
                  store=action_store,
                  cbfmt=action_cb_fmt,
                  cbz=action_cb_cvt,
                  cbsort=action_cb_sort,
                  cbcover=action_cb_cover,
                  cbtxt=action_txt_translate)

    parser = ArgumentParser(description="File handling manager")
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")

    subparsers = parser.add_subparsers(dest='subcmd', help='sub-command help')

    parser_check = subparsers.add_parser('check', help=action_check.__doc__)
    parser_check.add_argument('pth', help="Path to check. If pth is a dir, all files will be recursively checked")

    parser_store = subparsers.add_parser('store', help=action_store.__doc__)
    parser_store.add_argument('pth', help="Path to store. If pth is a dir, all files will be recursively checked")

    parser_fusion = subparsers.add_parser('fusion', help=action_fusion.__doc__)
    parser_fusion.add_argument('src', help="Path of source directory")
    parser_fusion.add_argument('dst', help="Path of destination directory")

    parser_fmt = subparsers.add_parser('fmt', help=action_fmt_names.__doc__)
    parser_fmt.add_argument('pth', help="Path to format. If pth is a dir, all file will be recursively formatted")

    parser_cbz = subparsers.add_parser('cbz', help=action_cb_cvt.__doc__)
    parser_cbz.add_argument('pth', help="Path to convert. If pth is a dir, all file will be recursively formatted")

    parser_cbfmt = subparsers.add_parser('cbfmt', help=action_cb_fmt.__doc__)
    parser_cbfmt.add_argument('pth', help="Path to format. If pth is a dir, all file will be recursively formatted")

    parser_cbsort = subparsers.add_parser('cbsort', help=action_cb_sort.__doc__)
    parser_cbsort.add_argument('pth', help="Path to sort. If pth is a dir, all file will be recursively formatted")

    parser_cbcover = subparsers.add_parser('cbcover', help=action_cb_cover.__doc__)
    parser_cbcover.add_argument('pth', help="Path to comics. If pth is a dir, all file will be recursively formatted")

    parser_txttrans = subparsers.add_parser('cbtxt', help=action_txt_translate.__doc__)

    kwds = vars(parser.parse_args())
    logging_tools.main(kwds.pop('verbosity'))

    # perform action
    subcmd = kwds.pop('subcmd')

    action[subcmd](**kwds)


if __name__ == '__main__':
    main()
