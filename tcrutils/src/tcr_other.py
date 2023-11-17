"""`other` submodule contains garbage or joke functions that never should be used in real code, just don't use this submodule pls. Why is it there? uhhh... :3."""
from collections.abc import Callable
from typing import Literal


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


sex = __import__('builtins').hex


def hex(number, leading_zeroes=2, *, upper=True):  # noqa: A001 # Intentional shadow
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
