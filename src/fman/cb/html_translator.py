"""Script to create a html description of the collection.
"""

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
thumb_dir = "zzthumbnails"
html_dir = "zzhtml"
tmp_fld = ".tmp_fld"


def create_thumbnail(book):
    filename = str(book)
    name, ext = splitext(filename)
    assert ext == ".cbz"

    dirname = std.dirname(filename)
    loc_thumbfile = join(thumb_dir, "{}/{}.jpg".format(dirname, filename))
    if not exists(loc_thumbfile):
        zf = ZipFile(book.filename, 'r')
        imgfiles = [name for name in zf.namelist() \
                    if splitext(name)[1].lower()[1:] in std.img_exts]
        imgfiles.sort()
        # imp = Parser()
        # imp.feed(zf.read(imgfiles[0]) )
        # img = imp.close()
        # zf.close()
        # hack because bug in ImageParser
        tmp_name = join(tmp_fld, "thumbnail" + splitext(imgfiles[0])[1].lower())
        tmpf = open(tmp_name, 'wb')
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


def book_size(book):
    filename = str(book)
    dirname = std.dirname(filename)

    size = stat(join(dirname, filename)).st_size

    return size / 1024 ** 2


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
            name = "{} - {}".format(name, book.title)
        else:
            name = book.title

    # find book size in Mo
    bs = book_size(book)

    # create li element
    txt = ["<li>"]
    txt.append("<h{:d}>{} ({:.1f} Mo)</h{:d}>".format(level, name, bs, level))
    kwds = "+".join(tuple(book.keywords()))
    txt.append("<a href='https://www.google.com/search?q=bd+{}'>".format(kwds))
    txt.append("<img src='../{}' tag='{}' />".format(quote(thumbname), quote(name)))
    txt.append("</a>")
    txt.append("</li>")

    return "\n".join(txt)


def serie_to_html(name, serie, level):
    txt = []
    txt.append("<li><h{:d}>{}</h{:d}>".format(level, name, level))
    txt.append("<ul>")

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
    if not exists(thumb_dir):
        mkdir(thumb_dir)

    for dirname in "0abcdefghijklmnopqrstuvwxyz":
        if not exists(join(thumb_dir, dirname)):
            mkdir(join(thumb_dir, dirname))

    if not exists(html_dir):
        mkdir(html_dir)

    if not exists(tmp_fld):
        mkdir(tmp_fld)

    ##################################################
    #
    print("create local html per directory")
    #
    ##################################################
    tpl = Template(resource_string("fman", "bd/template_main.html").decode("utf-8"))

    loc_htmls = []

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

        # create html file
        html_path = join(html_dir, "dir_{}.html".format(dirname))
        loc_htmls.append((dirname, html_path))

        # write book list
        keys = sorted(top.subseries.keys())

        body = ["<ul>"]

        for name in keys:
            print(name)
            serie = top.subseries[name]
            if isinstance(serie, Book):
                frag = book_to_html(serie, 1)
            else:
                frag = serie_to_html(name, serie, 1)
            body.append(frag)

        body.append("</ul>")

        with open(html_path, 'w') as f:
            txt = tpl.substitute(body="\n".join(body))
            f.write(txt)

    ##################################################
    #
    print("create main html index")
    #
    ##################################################
    body = ["<ul>"]
    for dir_name, file_name in loc_htmls:
        frag = "<li><a href='{}'>{}</a></li>".format(file_name, dir_name)
        body.append(frag)

    body.append("</ul>")

    with open("bddb.html", 'w') as f:
        txt = tpl.substitute(body="\n".join(body))
        f.write(txt)
