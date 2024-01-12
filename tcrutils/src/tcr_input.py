from collections.abc import Callable, Iterable, Mapping
from types import MappingProxyType
from typing import Any


def insist(func: Callable[[], Any], validator: Callable[[Any], bool] = bool):
  """### Keep invoking `func` until `validator(func())` returns Truey result, return it.

  # Use `functools.partial` for this!!!

  ```py
  from functools import partial
  number = int(insist(
    partial(input, "Input a number: "),
    partial(tcr.able, int)
  ))
  ```
  Keep in mind that insist won't convert the, str that was returned by `input()` in the above example, only verify its compliance with validator.
  """
  while True:
    result = func()
    if not validator(result): continue

    return result
