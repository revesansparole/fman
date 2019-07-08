"""Script used to sort cbz files in normalized directory architecture
and associate a hash file with them.
"""
from pathlib import Path

from ..standard import safe_rename


def rename_comics(pth, pattern, lang="en"):
    """Rename comics that follow a given pattern into numbered issues.

    Args:
      pth (Path): Path to files
      pattern (str): Initial name to keep afterward with numbers
      lang (str): Language suffix to append

    Returns:
      (None): rename in place
    """
    books = sorted(pth.glob(f"{pattern}*.cbz"))
    for i, book in enumerate(books):
        fmt_name = f"{pattern.lower()} - {i + 1:02d}.{lang}.cbz"
        safe_rename(book, fmt_name)
