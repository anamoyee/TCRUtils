import functools
import math
import typing as t
from collections.abc import Callable
from enum import Enum, auto
from functools import wraps

from ..src.tcr_compare import able
from ..src.tcr_run import run_sac
from .error import *


class _TT(Enum):
  TEXT = auto()
  PAREN_OPEN = auto()
  PAREN_CLOSE = auto()


class _Token:
  def __init__(self, type: _TT, value: str | None = None) -> None:
    self.type = type
    self.value = value

  def __repr__(self) -> str:
    return ('%s: %s' % (self.type.name, repr(self.value))) if self.value is not None else ('%s' % self.type.name)  # noqa: UP031


def _builder(x: str | bool) -> '_Token':
  if x is True:
    return _Token(_TT.PAREN_OPEN)
  elif x is False:
    return _Token(_TT.PAREN_CLOSE)
  elif isinstance(x, str):
    return _Token(_TT.TEXT, str(x))
  else:
    raise DynamicResponseSyntaxError(f'Unknown token type requested on build_placeholder_rich_return_value(): {x!r}')


def build_placeholder_rich_return_value(*args: str | bool) -> list[_Token]:
  """Build a value returnable from a placeholder callable, which can be used to insert a placeholder instead of a string.

  This does not validate input.
  - str: TEXT token
  - True: PAREN_OPEN token
  - False: PAREN_CLOSE token
  """
  return [_builder(x) for x in args]


def REQUIRE(*ctxs: str):
  """Require at least 1 of the given contexts to be present, otherwise raise DynamicResponsePlaceholderMissingContextError."""

  def decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      for ctx in ctxs:
        if ctx in kwargs and kwargs[ctx] is not None:
          for ctx in ctxs:
            if ctx not in kwargs:
              kwargs[ctx] = None
          return await run_sac(func, *args, **kwargs)
      raise DynamicResponsePlaceholderMissingContextError(f'One of {ctxs!r} must be present')

    return wrapper

  return decorator


def SWITCH(switch_name: str, *, remove: bool = True):
  """Append a bool context depending on whether or not the passed phrase is in args. Optionally remove it."""

  def decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      if switch_name in args:
        kwargs[switch_name] = True
      else:
        kwargs[switch_name] = False
      return await run_sac(func, *args, **kwargs)

    return wrapper

  return decorator


def rebuild_yourself(*args: str, __parens: tuple[str, str], __splitter: str, **_):
  """# Rebuild Yourself (RYS).

  Return the placeholder as text, as if it wasnt evaluated at all.
  For example {dummy} -> returns the str '{dummy}'. Therefore it looks like the placeholder wasnt evaluated.

  This requires at least __parens and __splitter built-in contexts but can take entire **contexts and void others.

  This also supports argumented placeholders for example: {div|1|0} # Division by 0 is invalid so your implementation may be to return the str '{div|1|0}' - although that's not a very good example (it'd be better to return some numeric value for consistency) it's one that ilustrates the point.
  """
  return f'{__parens[0]}{(__splitter.join(args))}{__parens[1]}'


def DEBUG_CATCH_ERRORS(func):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    try:
      return await run_sac(func, *args, **kwargs)
    except Exception as e:
      print(e)
      input()
      raise

  return wrapper


def REQUIRE_POSITIONAL(required_positionals: int, default: str | None = None):
  def decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      if len(args) < (required_positionals + 1):
        return default if default is not None else rebuild_yourself(*args, **kwargs)
      return await run_sac(func, *args, **kwargs)

    return wrapper

  return decorator


def STRINGIFY(func: Callable):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    return str(await run_sac(func, *args, **kwargs))

  return wrapper

def FLATTEN_IF_POSSIBLE(func: Callable):
  @wraps(func)
  async def wrapper(*args, **kwargs):
    return flatten_if_possible(await run_sac(func, *args, **kwargs))

  return wrapper

def flatten_if_possible(n: float | int) -> float | int:
  if n == int(n):
    return int(n)
  return n

def number(
  s: str,
  *,
  flatten_to_int_when_possible: bool = False,
  default: int | float = 0,
) -> float | int:
  if r := able(float, s):
    a = float(r.result)
    return flatten_if_possible(a)
  return default
