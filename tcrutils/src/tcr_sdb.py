import pathlib as p
import shelve
import shutil
import string
from collections.abc import Callable, Iterator
from typing import Any, Self

ALLOWED_CHARACTERS = string.ascii_letters + string.digits + "!&#'^~$,.%`{}[]();@_-+="  # Allowed characters in DB ID

DISALLOWED_SEQUENCES = (
  'PRN',
  'CON',
  'AUX',
  'NUL',
  'COM1',
  'COM2',
  'COM3',
  'COM4',
  'COM5',
  'COM6',
  'COM7',
  'COM8',
  'COM9',
  'COM0',
  'LPT1',
  'LPT2',
  'LPT3',
  'LPT4',
  'LPT5',
  'LPT6',
  'LPT7',
  'LPT8',
  'LPT9',
  'LPT0',
)


def c(a):
  return f'\x1b[{a}m'


A = f"""
{c("208")}class {c("39")}DB{c("7")}({c}{c(39)}tcr.ShelveDB{c("7")}){c}{c(231)}:
  {c(7)}directory {c(208)}= {c(46)}"/VALID/path/to/db/dir/" {c(8)}# Or pathlib.Path object{c}
"""[1:-1]


class ShelveDB(dict):
  """### Wrapper for shelve module databases.

  ```py
  class DB(tcr.ShelveDB):
    # REQUIRED:
    directory = "/VALID/path/to/db/dir/" # Or pathlib.Path object
    # OPTIONAL:
    defaults = {"r": list}
  ```
  ### Defaults:
  If key "r" is accessed but it's not found, return `list()` (that'd be a `[]`, not the `list` type itself of course!) and set the value at that key to it, so the next time it's looked up a value will be present, unless deleted or overwritten in the meantime.
  Values must be any zero-argument callables. (functions, classes/types, etc.).
  This is to avoid mutability problems, for each key a new instance is created.

  ## Raises:
    - ValueError: provided alnum_id is invalid.
    - RuntimeError: You did not or incorrectly set up the class declaration (shown above).
    - NotADirectoryError: The directory path you provided points to a file, not a directory or nothing.
  """

  directory: str | p.Path = None
  __directory: p.Path
  s: shelve.Shelf
  defaults: dict[Any, Callable[[], Any]] = None

  def __init__(self, alnum_id: str | int) -> None:
    if isinstance(self.directory, str | p.Path):
      if isinstance(self.directory, str):
        self.directory = p.Path(self.directory)
      self.__directory = self.directory
    else:
      raise RuntimeError('Set up the db as follows:\n' + A)  # noqa: TRY004

    if self.__directory.is_file():
      raise NotADirectoryError('Provide a path to a directory or a nonexistent path ' "(a directory will be created if it doesn't exist).")

    self.__directory.mkdir(exist_ok=True, parents=True)

    if self.defaults is None:
      self.defaults = {}

    if not all(callable(v) for v in self.defaults.values()):
      raise RuntimeError('All values of defaults must be callable.')

    if not all(char in ALLOWED_CHARACTERS for char in str(alnum_id)):
      raise ValueError(f'alnum_id must be any of those characters: {ALLOWED_CHARACTERS}')

    if str(alnum_id) in DISALLOWED_SEQUENCES:
      raise ValueError(f'alnum_id must not be any of theese: {", ".join(DISALLOWED_SEQUENCES)}')

    self.alnum_id = str(alnum_id)
    alnum_dirpath = self.__directory / self.alnum_id
    alnum_dirpath.mkdir(exist_ok=True)
    self.s = shelve.open(alnum_dirpath / self.alnum_id)

    super().__init__(self.s)

  def __getitem__(self, __key: Any) -> Any:
    try:
      return super().__getitem__(__key)
    except KeyError:
      if __key in self.defaults:
        val = self.defaults[__key]()
        self[__key] = val
        return val
      else:
        raise

  def __setitem__(self, __key: Any, __value: Any) -> None:
    self.s[__key] = __value
    self.s.sync()
    return super().__setitem__(__key, __value)

  def __delitem__(self, __key: Any) -> None:
    del self.s[__key]
    self.s.sync()
    return super().__delitem__(__key)

  def __del__(self) -> None:
    try:
      self.s.close()
    except AttributeError:
      return

  @property
  def d(self):
    """Convert the underlying shelf into a dictionary (make a copy as dict)."""
    return dict(self.s)  # .copy()

  def clear(self) -> None:
    """Clear both shelf and the underlying dictionary."""
    self.s.clear()
    self.s.sync()
    super().clear()

  def update(self, **kwargs: Any) -> None:
    """Update both the shelf and the underlying dictionary."""
    self.s.update(**kwargs)
    self.s.sync()
    super().update(**kwargs)

  def copy(self) -> dict:
    """Relinquishes the database connection and returns the underlying's dict copy."""
    return super().copy()

  def pop(self, *args, **kwargs) -> Any:
    super().pop(*args, **kwargs)
    res = self.s.pop(*args, **kwargs)
    self.s.sync()
    return res

  def popitem(self) -> tuple[Any, Any]:
    res = self.s.popitem()
    super().pop(res[0])
    self.s.sync()
    return res

  def setdefault(self, key, default=None):
    super().setdefault(key, default)
    res = self.s.setdefault(key, default)
    self.s.sync()
    return res

  def get_directory(self) -> p.Path:
    return self.__directory

  def get_path(self) -> p.Path:
    return self.get_directory() / self.alnum_id

  def drop_db(self) -> None:
    """Close the shelf and delete the underlying system directory of this database instance."""
    self.s.close()
    shutil.rmtree(self.__directory / self.alnum_id)

  @classmethod
  def iter_all(cls) -> Iterator[tuple[str, Self]]:
    for path in p.Path(cls.directory).iterdir():
      yield path.name, cls(path.name)

  @classmethod
  def iter_all_paths(cls) -> Iterator[p.Path]:
    yield from p.Path(cls.directory).iterdir()

  @classmethod
  def iter_all_path_names(cls) -> Iterator[str]:
    for path in p.Path(cls.directory).iterdir():
      yield path.name

  @classmethod
  def iter_all_shelves(cls) -> Iterator[Self]:
    for path in p.Path(cls.directory).iterdir():
      yield cls(path.name)

  @classmethod
  def exists(cls, alnum_id: str | int) -> bool:
    """Check if the given `alnum_id` is already in use (if a database directory exists and is a directory and is not empty)."""
    folder = p.Path(cls.directory) / str(alnum_id)
    return folder.is_dir() and (len(list(folder.iterdir())) > 0)  # Counting empty directories as non existent because theres no data
