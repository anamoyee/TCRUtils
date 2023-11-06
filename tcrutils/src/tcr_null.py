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

Null, _NullClass = Null(), Null

_NullClass.__new__ = _new
Null.__class__ = _NullClass

assert (Null) is (Null.__class__())  # No sneaky sneakies with making two different Nulls
