"""`other` submodule contains garbage or joke functions that never should be used in real code, just don't use this submodule pls. Why is it there? uhhh... :3."""
from typing import Literal


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

def hex(number, leading_zeroes=2, *, upper=True):  # noqa: A001 # Intentional shadow
    hex_output = __import__('builtins').hex(number)
    hex_value = hex_output[2:].zfill(leading_zeroes).upper() if upper else hex_output[2:].zfill(leading_zeroes)

    formatted_output = f"0x{hex_value}"
    if not upper:
        formatted_output = formatted_output.lower()

    return formatted_output
