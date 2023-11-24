import os
import pathlib as p
import re
from collections.abc import Callable


class path:
  """Provides path-related utilities."""

  @staticmethod
  def center(path: str | p.Path) -> p.Path:
    """Change directory to the location of the passed in __file__ (or any string path or pathlib Path). This will NOT detect if the passed in location is a directory, it will go to parent of it instead. Return previous path as a pathlib.Path object."""
    a = os.getcwd()
    os.chdir(p.Path(path).resolve().parent)
    return p.Path(a)

  @staticmethod
  def nextname(name='New folder') -> str:
    """If passed in name does not end with "`({int})" where `{int}` is any integer, return it with "` (1)`" appended else return it with the previously mentioned `{int}` incremented and leave it otherwise unchanged."""
    match = re.match(r'^(.*) \((\d+)\)$', name)

    if match:
      base_name = match.group(1)
      current_index = int(match.group(2))
      new_name = f'{base_name} ({current_index + 1})'
    else:
      new_name = f'{name} (1)'

    return new_name

  @staticmethod
  def newdir(
    name: str | None = None,
    path: p.Path | str | None = None,
    nextname: Callable[[str | None], str] = nextname,
  ) -> str:
    """Return unused directory or file with the name `name` in directory `path` or the current directory if not passed in."""
    if path is None:
      path = os.getcwd()
    path = str(path)
    listdir = os.listdir(path)
    while name in listdir:
      name = nextname(name)
    return name


__all__ = ['path']
