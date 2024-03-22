import inspect
from typing import TypeVar

T = TypeVar('T')


def get_caller_line_number(default: T | None = None) -> int | T:
  r = inspect.currentframe().f_back.f_lineno

  if r is None:
    return default

  return r
