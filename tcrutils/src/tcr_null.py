from typing import Any, Union


class Null:
  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return 'Null'


def or_(self, __value: Any) -> Union[Null, Any]:  # noqa: UP007
  return Union[Null, __value]  # noqa: UP007


def ror_(self, __value: Any) -> Union[Null, Any]:  # noqa: UP007
  return Union[Null, __value]  # noqa: UP007


def _new(cls, *args, **kwargs):
  return Null


Null.__or__ = or_
Null.__ror__ = ror_

Null, NullType = Null(), Null

NullType.__new__ = _new
Null.__class__ = NullType

assert (Null) is (Null.__class__())  # No sneaky sneakies with making two different Nulls


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
