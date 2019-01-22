from argparse import ArgumentParser, RawTextHelpFormatter
from glob import glob
from os import getcwd

from .fmt_name import fmt_names
from .fusion import compare, fusion
from .integrity_scripts import check, store
from .cb import fmt_name, txt_translator
from .cb.cvt_to_cbz import cvt_files
from .cb.editing import extract_covert
from .cb.sort_file import sort_comix


def action_cbcovert(*args, **kwds):
    """Generate one covert per comic book.
    """
    del kwds  # unused
    if len(args) == 0:
        filenames = sorted(glob("*.cbz"))
    else:
        filenames = args

    for fname in filenames:
        print(fname)
        extract_covert(fname)


def action_cbfmt(*args, **kwds):
    """Format name of comix book.
    """
    if len(args) == 0:
        fnames = None
    else:
        fnames = args
    del kwds  # unused
    fmt_name.main(fnames)


def action_cbsort(*args, **kwds):
    """Sort comic books in alphabetical folders.
    """
    if len(args) == 0:
        fnames = None
    else:
        fnames = args
    del kwds  # unused
    sort_comix(fnames)


def action_cbtxt(*args, **kwds):
    """Format comix list into txt.
    """
    del args  # unused
    del kwds  # unused
    txt_translator.main()


def action_cbz(*args, **kwds):
    """Convert comic books into cbz files.
    """
    if len(args) == 0:
        fnames = None
    else:
        fnames = args
    del kwds  # unused
    cvt_files(fnames)


def action_check(*args, **kwds):
    """Check whether files are still valid.
    """
    if len(args) == 0:
        fnames = ["."]
    else:
        fnames = args
    del kwds  # unused
    check(fnames)


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


def action_store(*args, **kwds):
    """Associate hash to filenames.
    """
    if len(args) == 0:
        fnames = ["."]
    else:
        fnames = args
    del kwds  # unused
    store(fnames)


action = dict(cbcovert=action_cbcovert,
              cbfmt=action_cbfmt,
              cbsort=action_cbsort,
              cbtxt=action_cbtxt,
              cbz=action_cbz,
              check=action_check,
              fmt=action_fmt_names,
              fusion=action_fusion,
              store=action_store)


def main():
    parser = ArgumentParser(description='File handling manager',
                            formatter_class=RawTextHelpFormatter)

    act_help = "type of action performed by fman, one of:\n"
    for name, func in action.items():
        act_help += "\n  - %s: %s" % (name, func.__doc__)

    parser.add_argument('action', metavar='action',
                        choices=tuple(action.keys()),
                        help=act_help)

    parser.add_argument('action_args', nargs='*',
                        help="List of files to perform action onto")

    parser.add_argument('-e', metavar='extra', nargs=2, action='append',
                        help='extra arguments to pass to the action',
                        dest='extra')

    args = parser.parse_args()
    if args.extra is None:
        extra = {}
    else:
        extra = dict(args.extra)

    action[args.action](*args.action_args, **extra)


if __name__ == '__main__':
    main()
