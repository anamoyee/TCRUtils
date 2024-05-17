"""Contains joke functions or the ones that will never be used in a serious situations/prod (This entire package sucks so much it should never be used in prod but uhhhhh.....)."""

from collections.abc import Callable
from typing import Any, Literal, Self

from ..src import tcr_cloud_imports as cloud_imports


def fizzbuzz(n: int) -> str: ...


fizzbuzz: Callable[[int], str] = lambda n: 'Fizz' * (n % 3 == 0) + 'Buzz' * (n % 5 == 0) or str(n)  # fmt: skip  # noqa: F811


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


def _cint_decorate_int_method(func):
  def wrapper(*args, **kwargs):
    result = func(*args, **kwargs)
    if isinstance(result, int):
      return CInt(result)
    else:
      return result

  return wrapper


class CInt:
  def __init__(self, value):
    self.value = value
    self.pos_flag = False
    self.neg_flag = False

  def __pos__(self):
    if self.pos_flag:
      self.value += 1
    self.pos_flag = not self.pos_flag
    return self

  def __neg__(self):
    if self.neg_flag:
      self.value -= 1
    self.neg_flag = not self.neg_flag
    return self

  def __eq__(self, other: Self | int) -> bool:
    if isinstance(other, CInt):
      return self.value == other.value
    else:
      return self.value == other

  def __int__(self):
    return self.value

  def __str__(self):
    return str(self.value)

  def __repr__(self) -> str:
    return self.__str__()

  def __tcr_fmt__(self, fmt_iterable, **kwargs):
    if self.neg_flag or self.pos_flag:
      return fmt_iterable(complex(int(self), 0.5 * (self.pos_flag - self.neg_flag)), **kwargs)
    else:
      return fmt_iterable(int(self), **kwargs)

  def __getattr__(self, name):
    if hasattr(self.value, name) and callable(getattr(self.value, name)):
      method = getattr(self.value, name)
      return _cint_decorate_int_method(method)
    else:
      raise AttributeError(f"'CInt' object has no attribute '{name}'")


class Private:
  """Makes every attribute private, like in other languages that support private/public attribute modifiers.

  Unfortunately i haven't gotten to writing a Public version of it so you can only private every single field :3

  Usage:
  ```py

  class PrivateString(Private, str): ...

  s = PrivateString('abc')

  print(s) # -> abc
  print(s.upper) # -> AttributeError: 'PrivateString' object has no attribute 'upper'
  print(s.__getattribute__) # -> AttributeError: 'PrivateString' object has no attribute '__getattribute__'

  ```
  """

  def __getattribute__(self, name):
    class_name = object.__getattribute__(self, '__class__').__name__
    raise AttributeError(f'{class_name!r} object has no attribute {name!r}')
