from .tcr_error import error


def commafy(text: str | int, splitter: str = ','):
  if isinstance(text, int) and text < 0:
    return '-' + commafy(-text)
  text = str(text)
  temp = ''
  for i, letter in enumerate(text[::-1]):
    temp += letter
    if i % 3 == 2 and i != len(text) - 1:
      temp += splitter
  return temp[::-1]


def nth(n: int):
  """Return a string containing original number + numeric suffix (st, nd, rd, th).

  Takes into account edge cases like 11, 12.
  Supports negative numbers & zero.

  Examples:
  ```py
  >>> nth(1)
  '1st'
  >>> nth(4)
  '4th'
  >>> nth(12)
  '12th'
  ```
  """
  if not isinstance(n, int):
    raise error.NotIntegerError(n)

  if n < 0:
    return '-' + nth(-n)

  if 10 < n % 100 < 14:
    suffix = 'th'
  else:
    match n % 10:
      case 1:
        suffix = 'st'
      case 2:
        suffix = 'nd'
      case 3:
        suffix = 'rd'
      case _:
        suffix = 'th'

  return str(n) + suffix
