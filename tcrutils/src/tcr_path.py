import os
import pathlib as p
import re
from collections.abc import Callable


def nextname(name):
  if name is None: name = "New folder"
  match = re.match(r'^(.*) \((\d+)\)$', name)

  if match:
      base_name = match.group(1)
      current_index = int(match.group(2))
      new_name = f"{base_name} ({current_index + 1})"
  else:
      new_name = f"{name} (1)"

  return new_name


class path:
  """Provides path-related utilities."""
  @staticmethod
  def newdir(name: str | None = None, path: p.Path | str | None = None, nextname: Callable[[str | None], str] = nextname):
    """Return unused directory or file with the name `name` in directory `path` or the current directory if not passed in."""
    if path is None: path = os.getcwd()
    path = str(path)
    listdir = os.listdir(path)
    while name in listdir:
      name = nextname(name)
    return name

__all__ = ['path']