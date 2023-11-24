"""`other` submodule contains garbage or joke functions that never should be used in real code, just don't use this submodule pls. Why is it there? uhhh... :3."""
from builtins import hex as sex
from collections.abc import Callable
from typing import Literal

from .tcr_color import c
from .tcr_constants import NEWLINE
from .tcr_null import Null


def oddeven(n: int | str) -> Literal['odd', 'even']:
  """### Outputs a string `'odd'` or `'even'` based on the supplied int `n`.

  ```py
  >>> from tcrutils.other import oddeven
  >>> oddeven(1)
  'odd'
  >>> oddeven(2)
  'even'
  """
  n = int(n)
  return 'eovdedn'[n % 2 :: 2]


def hex(number, leading_zeroes=2, *, upper=True):
  hex_output = sex(number)
  hex_value = (
    hex_output[2:].zfill(leading_zeroes).upper() if upper else hex_output[2:].zfill(leading_zeroes)
  )

  formatted_output = f'0x{hex_value}'
  if not upper:
    formatted_output = formatted_output.lower()

  return formatted_output


def commafy(text: str | int, splitter: str = ','):
  text = str(text)
  temp = ''
  for i, letter in enumerate(text[::-1]):
    temp += letter
    if i % 3 == 2 and i != len(text) - 1:
      temp += splitter
  return temp[::-1]


def intbool(__o: object, /):
  return int(bool(__o))


fizzbuz: Callable[[int], str] = lambda n: 'Fizz' * (n % 3 == 0) + 'Buzz' * (n % 5 == 0) or str(n)


def dir2(__o: object, /):
  return [x for x in dir(__o) if not x.startswith('__')]


def dir3(__o: object, /):
  return [x for x in dir(__o) if not x.startswith('_')]


def print_block(
  text: str,
  border_char: str = '#',
  *,
  margin: int = 1,
  border: int = 3,
  padding: int = 0,
  padding_top: int = 1,
  padding_bottom: int = 1,
  text_color: str = 'Gold',
  border_color: str = 'White',
  raw: bool = False,
  allow_invalid_config: bool = False,
) -> str | None:
  """Print or return a string of a "comment-like" block with text. Colors may optionally be set to `''` (empty string) to skip coloring of that part. Ends with a color reset unless none of the colors are enabled (both set to `''`).

  Params:
      - `margin`: The amount of spaces between the text and the inner walls (left-right only)
      - `border`: The width of walls (number of border_char characters, left-right only)
      - `padding`: The number of extra spaces added to the left of each line (left side only)
      - `padding_top` & `padding_bottom`: How many '\\n' characters to add at the beginning and the end of the string (top-bottom only)
  """

  text = str(text)

  if not allow_invalid_config and margin < 0 or border < 0 or padding < 0:
    msg = f'Invalid margin, border and/or padding(s) configuration {(margin, border, padding, padding_top, padding_bottom)!r}. Override this by passing in allow_invalid_config=True'
    raise ValueError(msg)

  if not allow_invalid_config and len(border_char) != 1:
    msg = f'border_char must be 1 character long (got {border_char!r} which is {len(border_char)!r} characters long). Override this by passing in allow_invalid_config=True'
    raise ValueError(msg)

  if text_color != '':
    text_color = c(text_color)
  if border_color != '':
    border_color = c(border_color)
  reset = c('reset')

  if not text_color and not border_color:
    reset = ''

  bar = f'{border_char * (border + margin + len(text) + margin + border)}'
  block = f"""
{padding_top * NEWLINE}{padding * ' '}{reset}{border_color}{bar}
{padding * ' '}{border * border_char}{reset}{margin * ' '}{text_color}{text}{reset}{margin * ' '}{border_color}{border * border_char}
{padding * ' '}{bar}{reset}{padding_bottom * NEWLINE}
"""[1:-1]
  if raw:
    return block

  print(block)
  return None
