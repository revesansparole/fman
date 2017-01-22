from os import remove
from os.path import exists, basename, join, dirname, splitext
from glob import glob


def clean(thumb_path):
    thumb_name = basename(thumb_path)
    bd_name = splitext(thumb_name)[0]
    dir_name = basename(dirname(thumb_path))
    bd_path = join(dir_name, bd_name)
    if not exists(bd_path):
        print("clean", thumb_path)
        remove(thumb_path)


thumb_dir = "zzthumbnails"

for dir_name in "0abcdefghijklmnopqrstuvwxyz":
    src = join(thumb_dir, dir_name)
    if exists(src):
        for filepath in sorted(glob(join(src, "*.jpg"))):
            clean(filepath)
