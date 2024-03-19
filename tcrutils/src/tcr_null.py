from types import UnionType
from typing import Any, Self, TypeVar, Union

from .tcr_class import Singleton


def instance(func):
  return func()


T = TypeVar('T')


class _NullLike:
  """Base class for null-like objects (Null, Undefined).

  Can be bitwise-ored with any other value to yield that other value. (If both values in bitwise or are null-like, return the directionally right one)
  """

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return self.__class__.__name__

  def __bool__(self):
    return False

  def __or__(self, __value: T) -> T:
    return __value

  def __ror__(self, __value: T) -> T:
    return __value


@instance
class Null(Singleton, _NullLike):
  """Value is explicitly declared as absent."""


@instance
class Undefined(Singleton, _NullLike):
  """Value is missing."""


class UniqueDefault:
  """Used as a default parameter for the parameter named default (yeah i know that's uh... let's just see the example).

  Example:
  ```py
  from tcrutils import UniqueDefault as RaiseError

  def get_something(..., *, default: Any | RaiseError = RaiseError):
  ... # Function implementation

  # Nothing was found, falling to raising error or returning default value if such was specified.
  if default is not RaiseError:
    return default
  raise KeyError("Unable to find something.")
  """
