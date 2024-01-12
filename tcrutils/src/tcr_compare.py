"""Functions related to comparisons, didn't want to name the file tcr_test.py to avoid confusion with testing as in testing if code works."""

from collections.abc import Callable
from typing import Any


def able(func: Callable, *args, able_exception__: BaseException = Exception, **kwargs):
  """### Return True if x is func(x)-able aka does not raise any errors while passed in to func otherwise return False.

  This does not return the result, only bool whether it didn't raise an error in the process.

  #### Example:
  ```py
  >>> able(int, '1') # Wouldn't raise any Exception
  True
  >>> able(int, 'a') # Would raise: ValueError: invalid literal for int() with base 10: 'a'
  False
  >>> [int(x) for x in [] if able(int, x)]
  ```
  """
  try:
    func(*args, **kwargs)
  except able_exception__:
    return False
  else:
    return True
