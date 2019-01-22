"""
Base setting for logging in the package.
This module is executed when importing pkglts.
"""
import logging
import logging.handlers


def main(verbosity):
    """Set logging configuration.

    Args:
        verbosity (int): verbosity level

    Returns:
        None
    """
    if verbosity > 2:
        verbosity = 2
    vlevel = [logging.WARNING, logging.INFO, logging.DEBUG][verbosity]

    fmt = logging.Formatter('%(asctime)s %(levelname)s (%(name)s): %(message)s')

    wng_ch = logging.StreamHandler()
    wng_ch.setLevel(vlevel)
    wng_ch.setFormatter(fmt)

    logger = logging.getLogger("fman")
    logger.setLevel(vlevel)
    logger.addHandler(wng_ch)


if __name__ == '__main__':
    main(0)
