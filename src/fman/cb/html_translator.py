"""Script to create a html description of the collection.
"""

from pathlib import Path
from glob import glob
from os import mkdir, stat
from os.path import splitext, exists, join
from PIL import Image
# from ImageFile import Parser
from pkg_resources import resource_string
from string import Template
from urllib.parse import quote
from zipfile import ZipFile

from .book import Serie, Book
from . import standard as std

thumb_width = 80
thumb_dir = Path("zzthumbnails")
html_dir = Path("zzhtml")
tmp_fld = Path(".tmp_fld")


def create_thumbnail(book):
    filename = str(book)
    assert book.filename.suffix == ".cbz"

    dirname = std.dirname(filename)
    loc_thumbfile = thumb_dir / f"{dirname}/{filename}.jpg"
    if not loc_thumbfile.exists():
        zf = ZipFile(book.filename, 'r')
        imgfiles = [name for name in zf.namelist() if name.split(".")[-1].lower() in std.img_exts]
        imgfiles.sort()
        # imp = Parser()
        # imp.feed(zf.read(imgfiles[0]) )
        # img = imp.close()
        # zf.close()
        # hack because bug in ImageParser
        tmp_name = tmp_fld / f"thumbnail.{imgfiles[0].split('.')[-1].lower()}"
        tmpf = open(str(tmp_name), 'wb')
        tmpf.write(zf.read(imgfiles[0]))
        tmpf.close()
        zf.close()
        img = Image.open(tmp_name)
        img.load()
        if img.mode != 'RGB':
            img = img.convert('RGB')

        w, h = img.size
        thumb = img.resize((thumb_width, int(h * float(thumb_width) / w)))
        thumb.save(loc_thumbfile)

    # return
    return loc_thumbfile


def book_to_html(book, level):
    print("\t", book)

    # create thumbnail
    thumbname = create_thumbnail(book)
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
    bs = std.book_size(book)

    # create li element
    kwds = "+".join(tuple(book.keywords()))
    txt = [
        "<li>",
        f"<h{level:d}>{name} ({bs:.1f} Mo)</h{level:d}>",
        f"<a href='https://www.google.com/search?q=bd+{kwds}'>",
        f"<img src='../{quote(str(thumbname))}' tag='{quote(name)}' />",
        "</a>",
        "</li>"
    ]

    return "\n".join(txt)


def serie_to_html(name, serie, level):
    txt = [
        f"<li><h{level:d}>{name}</h{level:d}>",
        "<ul>"
    ]

    for name in sorted(serie.subseries.keys()):
        txt.append(serie_to_html(name, serie.subseries[name], level + 1))

    books = [(str(book), book) for book in serie.books]
    for name, book in sorted(books):
        txt.append(book_to_html(book, level + 1))

    txt.append("</ul>")
    txt.append("</li>")

    return "\n".join(txt)


def main():
    ##################################################
    #
    print("create directories")
    #
    ##################################################
    folders = [thumb_dir, html_dir, tmp_fld] + [thumb_dir / n for n in "0abcdefghijklmnopqrstuvwxyz"]
    for fld in folders:
        if not fld.exists():
            fld.mkdir()

    ##################################################
    #
    print("create local html per directory")
    #
    ##################################################

    tpl = Template((Path(__file__).parent / "template_main.html").read_text(encoding="utf-8"))

    loc_htmls = []

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

        # create html file
        html_pth = html_dir / f"dir_{dirname}.html"
        loc_htmls.append((dirname, html_pth))

        # write book list
        body = ["<ul>"]

        for name in sorted(top.subseries.keys()):
            print(name)
            serie = top.subseries[name]
            if isinstance(serie, Book):
                frag = book_to_html(serie, 1)
            else:
                frag = serie_to_html(name, serie, 1)
            body.append(frag)

        body.append("</ul>")

        with open(str(html_pth), 'w') as f:
            txt = tpl.substitute(body="\n".join(body))
            f.write(txt)

    ##################################################
    #
    print("create main html index")
    #
    ##################################################
    body = ["<ul>"]
    for dir_name, pth in loc_htmls:
        frag = f"<li><a href='{pth}'>{dir_name}</a></li>"
        body.append(frag)

    body.append("</ul>")

    with open("bddb.html", 'w') as f:
        txt = tpl.substitute(body="\n".join(body))
        f.write(txt)
