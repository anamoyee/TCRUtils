import os
import pathlib as p
import re as regex
import string
from typing import Any, Literal, NoReturn

from ..src.tcr_compare import able
from ..src.tcr_constants import BACKTICKS
from ..src.tcr_null import UniqueDefault as RaiseError
from .tcrd_snowflake import is_snowflake


def get_token(filename: str = 'TOKEN.txt', depth=2, *, dont_strip=False, default=RaiseError) -> None | str:
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


def _ify_snowflake_errorer(id: Any) -> None:
  if not is_snowflake(id, allow_string=True):
    if isinstance(id, int | str):
      err = ValueError('id is not a valid snowflake, use tcr.discord.is_snowflake() to validate if needed.')
    else:
      err = TypeError(f'Expected str or int, got {type(id)} instead.')

    raise err


class IFYs:
  """Features related to turning IDs into user/channel/command/etc. mentions, emojis, and more if i can think of any.

  https://discord.com/developers/docs/reference#message-formatting

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
  def userify(user_id: int | str) -> str:
    """### User mentions.

    ```py
    >>> IFYs.userify(1234)
    '<@1234>'
    ```
    """

    _ify_snowflake_errorer(user_id)

    return f'<@{user_id}>'

  @staticmethod
  def userbangify(user_id: int | str) -> str:
    """### User mentions (Old discord system).

    ```py
    >>> IFYs.userbangify(1234)
    '<@!1234>'
    ```
    """

    _ify_snowflake_errorer(user_id)

    return f'<@!{user_id}>'

  @staticmethod
  def channelify(channel_id: int | str) -> str:
    """### Channel mentions.

    ```py
    >>> IFYs.channelify(1234)
    '<#1234>'
    ```
    """

    _ify_snowflake_errorer(channel_id)

    return f'<#{channel_id}>'

  @staticmethod
  def roleify(role_id: int | str) -> str:
    """### Role mentions.

    ```py
    >>> IFYs.roleify(1234)
    '<@&1234>'
    ```
    """

    _ify_snowflake_errorer(role_id)

    return f'<@&{role_id}>'

  @staticmethod
  def commandify(command_name: str, command_id: int | str) -> str:
    """### Command mentions.

    I'm not sure how to validate `command_name` other than the type (python regex apparently doesn't support whatever discord wrote [here](https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-naming))

    ```py
    >>> IFYs.commandify('settings', 1234)
    '</settings:1234>'
    ```
    """

    _ify_snowflake_errorer(command_id)

    if not isinstance(command_name, str):
      raise TypeError(f'Expected str, got {type(command_name)} instead.')

    return f'</{command_name}:{command_id}>'

  @staticmethod
  def emojify(emoji_name: str, emoji_id: int | str, *, animated: bool = False) -> str:
    """### Emojis (animated and non-animated).

    I'm not sure how to validate `emoji_name` other than the type (i'm not aware of discord's emoji naming scheme unlime command_name where they at least published some regex? maybe they did somewhere but if they did as i said im not aware of it).

    ```py
    >>> IFYs.emojify('mmLol', 1234)
    '<:mmLol:1234>'
    >>> IFYs.emojify('b1nzy', 1234, animated=True)
    '<a:b1nzy:1234>'
    ```
    """

    _ify_snowflake_errorer(emoji_id)

    if not isinstance(emoji_name, str):
      raise TypeError(f'Expected str, got {type(emoji_name)} instead.')

    return f'<{"a" if animated else ""}:{emoji_name}:{emoji_id}>'

  @staticmethod
  def timeify(timestamp: int | str, style: None | Literal['t', 'T', 'd', 'D', 'f', 'F', 'R'] = None) -> str:
    if not able(int, timestamp):
      raise TypeError(f'Expected intable object, got {f"{type(timestamp)} (but a str that does not contain an int)" if isinstance(timestamp, str) else type(timestamp)} instead.')

    if style not in (None, 't', 'T', 'd', 'D', 'f', 'F', 'R'):
      raise ValueError(f'Expected style=None, or a valid format specifier (https://discord.com/developers/docs/reference#message-formatting-timestamp-styles)')

    return f'<t:{timestamp}{":" if style is not None else ""}{style if style is not None else ""}>'

  @staticmethod
  def specialify(option: Literal['customize', 'browse', 'guide'] = 'customize') -> str:
    if option not in ('customize', 'browse', 'guide'):
      raise ValueError(f"Expected option in ('customize', 'browse', 'guide'), got {option} instead.")

    return f'<id:{option}>'
