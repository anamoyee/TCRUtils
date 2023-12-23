"""Functions related to comparisons, didn't want to name the file tcr_test.py to avoid confusion with testing as in testing if code works."""


def able(func, x, *, exception: BaseException = Exception):
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
  try: ...
  except exception:
    return False
  return True
