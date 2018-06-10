"""Script to create a txt description of the collection.
"""

from glob import glob
from os import mkdir, stat
from os.path import exists, join

from .book import Serie, Book
from . import standard as std

txt_dir = "zztxt"


def book_size(book):
    filename = str(book)
    dirname = std.dirname(filename)

    size = stat(join(dirname, filename)).st_size

    return size / 1024 ** 2


def book_to_txt(book, level):
    print("\t", book)

    # create book name
    if len(book.number) > 0:
        name = book.number
    else:
        name = ""

    if len(book.title) > 0:
        if len(name) > 0:
            name = "{} - {}".format(name, book.title)
        else:
            name = book.title

    # find book size in Mo
    bs = book_size(book)

    # create element
    pre = "\t" * level
    txt = []
    txt.append(pre + "{} ({})({:.1f} Mo)".format(name, book.language, bs))

    return "\n".join(txt)


def serie_to_txt(name, serie, level):
    txt = ["\t" * level + "{}:".format(name)]

    for name in sorted(serie.subseries.keys()):
        txt.append(serie_to_txt(name, serie.subseries[name], level + 1))

    books = [(str(book), book) for book in serie.books]
    for name, book in sorted(books):
        txt.append(book_to_txt(book, level + 1))

    return "\n".join(txt)


def main():
    ##################################################
    #
    print("create directories")
    #
    ##################################################
    if not exists(txt_dir):
        mkdir(txt_dir)

    ##################################################
    #
    print("write txt")
    #
    ##################################################
    for dirname in "0abcdefghijklmnopqrstuvwxyz":
        filenames = sorted(glob(join(dirname, "*.cbz")))

        # sort by serie
        top = Serie()

        for filepath in filenames:
            book = Book(filepath)
            if len(book.serie) == 0:
                # single issue
                top.subseries[book.title] = book
            else:
                # serie, may be recursive with sub series
                gr = book.serie.split(" - ")
                ser = top
                for name in gr:
                    try:
                        ser = ser.subseries[name]
                    except KeyError:
                        ser.subseries[name] = Serie()
                        ser = ser.subseries[name]

                ser.books.append(book)

        # write book list
        keys = sorted(top.subseries.keys())

        body = ["<DIRECTORY>"]

        for name in keys:
            print(name)
            serie = top.subseries[name]
            if isinstance(serie, Book):
                frag = book_to_txt(serie, 0)
            else:
                frag = serie_to_txt(name, serie, 0)
            body.append(frag)

        body.append("</DIRECTORY>")

        # create txt file
        txt_path = join(txt_dir, "dir_{}.txt".format(dirname))
        with open(txt_path, 'w') as f:
            f.write("\n".join(body))
