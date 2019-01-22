"""Script to create a txt description of the collection.
"""

from pathlib import Path

from .book import Book, Serie

txt_dir = Path("zztxt")


def book_size(book):
    """Size of file associated to book.

    Args:
        book (Book): book object

    Returns:
        (float): size in [Mo]
    """
    size = book.filename.stat().st_size

    return size / 1024 ** 2


def book_to_txt(book, level):
    """Convert a single book to text paragraph

    Args:
        book (Book): book object
        level (int): sublevel

    Returns:
        (str)
    """
    print("\t", book)

    # create book name
    if len(book.number) > 0:
        name = book.number
    else:
        name = ""

    if len(book.title) > 0:
        if len(name) > 0:
            name = f"{name} - {book.title}"
        else:
            name = book.title

    # find book size in Mo
    bs = book_size(book)

    return "\t" * level + f"{name} ({book.language})({bs:.1f} Mo)"


def serie_to_txt(name, serie, level):
    """Convert a serie into text paragraph

    Args:
        name (str): name of book
        serie (Serie): set of book
        level (int): sublevel

    Returns:
        (str)
    """
    txt = ["\t" * level + f"{name}:"]

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
    if not txt_dir.exists():
        txt_dir.mkdir()

    ##################################################
    #
    print("write txt")
    #
    ##################################################
    for dirname in "0abcdefghijklmnopqrstuvwxyz":
        dir_pth = Path(dirname)

        # sort by serie
        top = Serie()

        for pth in dir_pth.glob("*.cbz"):
            book = Book(pth)
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
        body = ["<DIRECTORY>"]

        for name in sorted(top.subseries.keys()):
            print(name)
            serie = top.subseries[name]
            if isinstance(serie, Book):
                frag = book_to_txt(serie, 0)
            else:
                frag = serie_to_txt(name, serie, 0)
            body.append(frag)

        body.append("</DIRECTORY>")

        # create txt file
        txt_pth = txt_dir / f"dir_{dirname}.txt"
        with open(str(txt_pth), 'w') as f:
            f.write("\n".join(body))
