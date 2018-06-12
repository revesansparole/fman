from argparse import ArgumentParser
from os import getcwd
from pathlib import Path

from . import logging_tools
from .fmt_name import fmt_names
from .fusion import compare, fusion
from .integrity_scripts import check, store


def action_check(**kwds):
    """Check whether files are still valid.
    """
    pth = Path(kwds['pth'])
    check(pth)


def action_fmt_names(*args, **kwds):
    """Rename files with normalized names.
    """
    if len(args) == 0:
        fnames = ["."]
    else:
        fnames = args
    del kwds  # unused
    fmt_names(fnames)


def action_fusion(*args, **kwds):
    """Attempt to fusion the content of two directories.
    """
    if len(args) == 0:
        raise UserWarning("I need at least a destination directory")
    elif len(args) == 1:
        src_dir = getcwd()
        dst_dir = args[0]
    else:
        src_dir, dst_dir = args[:2]
    del kwds  # unused

    conflicts = fusion(src_dir, dst_dir)

    for names in conflicts:
        compare(*names)


def action_store(**kwds):
    """Associate hash to files.
    """
    pth = Path(kwds['pth'])
    store(pth)


def main():
    """Run CLI evaluation"""
    action = dict(check=action_check,
                  fmt=action_fmt_names,
                  fusion=action_fusion,
                  store=action_store)

    parser = ArgumentParser(description="File handling manager")
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase output verbosity")

    subparsers = parser.add_subparsers(dest='subcmd', help='sub-command help')

    parser_check = subparsers.add_parser('check', help=action_check.__doc__)
    parser_check.add_argument('pth', help="Path to check. If pth is a dir, all files will be recursively checked")

    parser_store = subparsers.add_parser('store', help=action_store.__doc__)
    parser_store.add_argument('pth', help="Path to store. If pth is a dir, all files will be recursively checked")

    kwds = vars(parser.parse_args())
    logging_tools.main(kwds.pop('verbosity'))

    # perform action
    subcmd = kwds.pop('subcmd')

    action[subcmd](**kwds)


if __name__ == '__main__':
    main()
