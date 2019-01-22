"""Main Book class that hold info on a cbz file based on it's filename.
"""

import re

from unidecode import unidecode

nb_fmt1 = "^([0-9]+)$"
nb_fmt2 = "^([0-9]+.[0-9]+)$"
nb_fmt3 = "^([0-9]+.[0-9]+)$"
nb_fmt4 = "^(hs[0-9]?)$"

# number_re = re.compile(r"^(hs)?[0-9]?(.[0-9]+)?(-[0-9]+)?$")
number_re = re.compile("|".join((nb_fmt1, nb_fmt2, nb_fmt3, nb_fmt4)))

articles = ("les", "la", "une", "un", "l'", "le", "des", "the")


def _find_number_pos(items):
    for i in range(len(items) - 1, -1, -1):
        if number_re.match(items[i]) is not None:
            return i

    return None


def move_article(name):
    """If name starts with an article, move
    it at the end of name.

    Examples:
        'la tour prend garde' -> 'tour prend garde, la'

    Args:
        name (str):

    Returns:
        (str): formatted name
    """
    gr = name.split(" - ")

    if gr[0].startswith("l'"):
        gr[0] = "%s, l'" % (gr[0][2:])

    elif " " in gr[0]:
        first, last = gr[0].split(" ", 1)
        if first in articles:
            gr[0] = "%s, %s" % (last, first)

    return " - ".join(gr)


class Serie(object):
    """a simple container
    """

    def __init__(self):
        self.subseries = {}
        self.books = []


class Book(object):
    """A single issue of a BD
    """

    def __init__(self, pth):
        """Construct a Book object

        Args:
            pth (Path): path to book file, only name will be kept
        """
        self.filename = pth
        self.serie = ""  # serie's name
        self.number = ""  # issue number (dd, ddd, dddd.dd, dd-dd, hs, hsdd)
        self.title = ""  # name of this issue
        self.language = None  # digram for country e.g. 'fr' or 'en'
        self.type = None  # file type
        name = pth.name.lower().replace("_", " ")
        name = unidecode(name)
        self.analyse(name)

    def __str__(self):
        """construct a formatted filename for this issue
        """
        frags = []

        # serie
        if len(self.serie) > 0:
            frags.append(self.serie)
            if len(self.number) > 0:
                frags.append(self.number)

        # title
        if len(self.title) > 0:
            frags.append(self.title)

        # language
        lang = self.language

        # type
        typ = self.type

        return "{}.{}.{}".format(" - ".join(frags), lang, typ)

    def analyse(self, name):
        """analyse a name to construct this object
        """
        # type
        gr = name.split(".")
        if len(gr) == 0:
            raise UserWarning("no extension?")

        self.type = gr[-1]

        # language
        if gr[-2] in ('fr', 'en', 'it'):
            self.language = gr[-2]
            name = ".".join(gr[:-2])
        else:
            self.language = 'en'
            name = ".".join(gr[:-1])

        # title and serie
        gr = name.split(" - ")
        if len(gr) == 1:
            self.serie = ""
            self.number = ""
            self.title = name
        else:
            # find position of number descr
            i = _find_number_pos(gr)
            if i is None:
                self.serie = gr[0]
                self.number = ""
                self.title = " - ".join(gr[1:])
            else:
                self.serie = " - ".join(gr[:i])
                self.number = gr[i]
                self.title = " - ".join(gr[(i + 1):])

        # reformat serie or title
        if len(self.serie) > 0:
            self.serie = move_article(self.serie)
        elif len(self.title) > 0:
            self.title = move_article(self.title)

    def keywords(self):
        """Return names in serie and title as a list of keywords
        """
        for s in " ".join((self.serie, self.title)).split(" "):
            if s not in articles and s != "-" and len(s) > 2:
                if s[-1] == ",":
                    yield s[:-1]
                else:
                    yield s
