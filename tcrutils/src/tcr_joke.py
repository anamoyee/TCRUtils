"""Contains joke functions or the ones that will never be used in a serious situations."""

from collections.abc import Callable
from typing import Literal

fizzbuzz: Callable[[int], str] = lambda n: 'Fizz' * (n % 3 == 0) + 'Buzz' * (n % 5 == 0) or str(n)


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


def christmas_tree(*, height=10, symbol='*'):
  """Generate a christmas tree for printing in a console.

  Height is the number of lines the tree will have.\\
  Symbol is any 1-2 long string for example 'C#' or '*'.
  """
  if len(symbol) == 1:
    symbol = 2 * symbol

  def transform(symbols: str):
    return symbols.center(height * 2, ' ')

  return '\n'.join([transform(symbol * x) for x in range(height + 1) if x])
