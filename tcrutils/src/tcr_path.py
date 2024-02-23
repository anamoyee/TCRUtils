import inspect
import os
import pathlib as p
import re
from collections.abc import Callable

from .tcr_console import console


class path:
  """Provides path-related utilities."""

  @staticmethod
  def center(path: str | p.Path) -> p.Path:
    """### Change directory to the location of the passed in __file__ (or any string path or pathlib Path). This will NOT detect if the passed in location is a directory, it will go to parent of it instead. Return previous path as a pathlib.Path object.

    This function is shit use tcr.path.thisdir() instead.
    """
    a = os.getcwd()
    os.chdir(p.Path(path).resolve().parent)
    return p.Path(a)

  @staticmethod
  def nextname(name='New folder') -> str:
    """### If passed in name does not end with "`({int})" where `{int}` is any integer, return it with "` (1)`" appended else return it with the previously mentioned `{int}` incremented and leave it otherwise unchanged."""
    match = re.match(r'^(.*) \((\d+)\)$', name)

    if match:
      base_name = match.group(1)
      current_index = int(match.group(2))
      new_name = f'{base_name} ({current_index + 1})'
    else:
      new_name = f'{name} (1)'

    return new_name

  @staticmethod
  def nextname_file_ext_fix(name='New file.txt') -> str:
    match = re.match(r'^(.*?)(?:\s*\((\d+)\))?(?:\.(\w+))?$', name)
    if not match:
      raise ValueError('Invalid filename format')

    base_name, number, extension = match.groups()

    new_number = int(number) + 1 if number else 1

    return f'{base_name} ({new_number}).{extension}' if extension else f'{base_name} ({new_number})'

  @staticmethod
  def newdir(
    name: str | None = None,
    path: p.Path | str | None = None,
    nextname: Callable[[str | None], str] = nextname,
  ) -> str:
    """### Return unused directory or file with the name `name` in directory `path` or the current directory if not passed in."""
    if path is None:
      path = os.getcwd()
    path = str(path)
    listdir = os.listdir(path)
    while name in listdir:
      name = nextname(name)
    return name

  @staticmethod
  def thisdir(*, chdir=False) -> p.Path:
    """### Return the directory of the furthest back file in the callstack as pathlib.Path, optionally navigate to it with os.chdir()."""
    frames = inspect.stack()
    pth = frames[-1].filename  # Get the filename of the furthest back frame
    pth = p.Path(pth).parent
    if chdir:
      os.chdir(pth)
    return pth

  @staticmethod
  def nt_validname(nt_objname: str | p.Path) -> bool:
    """### Return True if the passed in `nt_objname` is a valid NT File/Folder/whatever, else return False.

    This does NOT check if the path exists.
    ### The passed in path is stripped(), the used one should be as well!
    """
    if not isinstance(nt_objname, str):
      nt_objname: str = str(nt_objname.absolute().name)

    return bool((all((x not in nt_objname) for x in ('\n', '\r'))) and (nt_objname.strip() not in ('', '.', '..')) and (re.match(r'^[^<>:"\/\\|?*\n]*$', nt_objname.strip())))


__all__ = ['path']
