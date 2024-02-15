import os
import pathlib as p
import re as regex
from typing import Literal, NoReturn

from ..src.tcr_compare import able
from ..src.tcr_constants import BACKTICKS
from ..src.tcr_null import UniqueDefault as RaiseError
from .tcrd_snowflake import is_snowflake


def get_token(
  filename: str = 'TOKEN.txt', depth=2, *, dont_strip=False, default=RaiseError
) -> None | str:
  """Get the nearest file with name=filename (default 'TOKEN.txt') and return its stripped contents (unless specified not to strip with `dont_strip=True`).

  This algoritm searches for files named TOKEN.txt (or custom name) in the current directory, then the parent directory, then the parent of parent and so on.
  The search continues up to depth `depth` (depth=0: current directory only, depth=1, current directory and its parent, etc.). If multiple files are found, return the closest one to the current directory.
  If no file is found, an error will be raised unless `default` is provided.
  """

  def rexit(x):
    os.chdir(origin_path)
    return x

  origin_path = p.Path.cwd().absolute()

  os.chdir(origin_path)

  f = origin_path / filename

  for i in range(depth + 1):
    f = (origin_path / '/'.join(['..'] * i)) / filename
    if f.is_file():
      t = f.read_text()
      if not dont_strip:
        t = t.strip()
      return rexit(t)

  if default is not RaiseError:
    return default

  raise FileNotFoundError(f'Unable to locate token file: {filename}')


class IFYs:
  """Features related to turning IDs into user/channel/command/etc. mentions, emojis, and more if i can think of any.

  Example:
  ```py
  >>> IFYs.userify(1234)
  '<@1234>'
  ```

  Includes argument validation:
  - Raises TypeError if invalid type was supplied (not str or int)
  - Raises ValueError if the type is valid, but snowflake in it is not (for example if negative int was passed in)
  """

  @staticmethod
  def userify(user_id: int | str):
    """### User mentions.

    ```py
    >>> IFYs.userify(1234)
    '<@1234>'
    ```
    """

    if not is_snowflake(user_id, allow_string=True):
      if isinstance(user_id, int | str):
        err = ValueError(
          'user_id is not a valid snowflake, use tcr.discord.is_snowflake() to validate if needed.'
        )
      else:
        err = TypeError(f'Expected str or int, got {type(user_id)} instead.')

      raise err

    return f'<@{user_id}>'

  @staticmethod
  def channelify(channel_id: int | str):
    """### User mentions.

    ```py
    >>> IFYs.channelify(1234)
    '<#1234>'
    ```
    """

    if not is_snowflake(channel_id, allow_string=True):
      if isinstance(channel_id, int | str):
        err = ValueError(
          'channel_id is not a valid snowflake, use tcr.discord.is_snowflake() to validate if needed.'
        )
      else:
        err = TypeError(f'Expected str or int, got {type(channel_id)} instead.')

      raise err

    return f'<#{channel_id}>'
