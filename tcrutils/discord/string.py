import os
import pathlib as p
import re as regex
from typing import Literal, NoReturn

from ..src.tcr_compare import able
from ..src.tcr_constants import BACKTICKS
from .validate import is_snowflake


def get_token(filename: str = 'TOKEN.txt', depth=2) -> None | str:
  """Get the nearest file with name=filename (default 'TOKEN.txt') and return its stripped contents.

  This algoritm searches for files named TOKEN.txt (or custom name) in the current directory, then the parent directory, then the parent of parent and so on.
  The search continues up to depth `depth` (depth=0: current directory only, depth=1, current directory and its parent, etc.). If multiple files are found, return the closest one to the current directory.
  """
  def rexit(x):
    os.chdir(origin_path)
    return x

  origin_path = p.Path.cwd().absolute()

  print(origin_path)

  os.chdir(origin_path)

  f = (origin_path / filename)

  for i in range(depth+1):
    f = ((origin_path / '/'.join(['..'] * i)) / filename)
    if f.is_file():
      return rexit(f.read_text().strip())

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
        err = ValueError('user_id is not a valid snowflake, use tcr.discord.is_snowflake() to validate if needed.')
      else:
        err = TypeError(f"Expected str or int, got {type(user_id)} instead.")

      raise err

    return f"<@{user_id}>"

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
        err = ValueError('channel_id is not a valid snowflake, use tcr.discord.is_snowflake() to validate if needed.')
      else:
        err = TypeError(f"Expected str or int, got {type(channel_id)} instead.")

      raise err

    return f"<#{channel_id}>"
