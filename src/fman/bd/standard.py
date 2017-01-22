"""Defines standard paths and components for the library.
"""


def dirname(cbzname):
    dname = cbzname[0]
    if dname in "0123456789":
        dname = "0"

    return dname


# extension of files recognized as images
img_exts = ("jpg", "jpeg", "jp2", "png", "ppm", "gif")
