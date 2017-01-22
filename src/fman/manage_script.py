from argparse import ArgumentParser, RawTextHelpFormatter

from integrity_scripts import check, store


def action_check(*args, **kwds):
    """Check whether files are still valid.
    """
    if len(args) == 0:
        fnames = ["."]
    else:
        fnames = args
    del kwds  # unused
    check(fnames)


def action_store(*args, **kwds):
    """Associate hash to filenames.
    """
    if len(args) == 0:
        fnames = ["."]
    else:
        fnames = args
    del kwds  # unused
    store(fnames)


action = dict(check=action_check,
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
                        help="action to perform on files")

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
