from collections.abc import Iterable

from .tcr_other import hex


def print_iterable(
  it: Iterable, *, recursive=True, raw=False
) -> str | None:  # Required for debugging (console object)
  """Print an iterable in a nicely formatted way. If raw=True return the nicely formatted string instead of printing.

  Supports lists, tuples, sets, dicts, strings, generators, bytestrings, bytearrays and may work with other Iterables
  """
  if it == []:
    if not raw:
      print('[]')
      return it
    return '[]'

  if it == ():
    if not raw:
      print('()')
      return it
    return '()'

  if it == {}:
    if not raw:
      print('{}')
      return it
    return '{}'

  if it == set():
    if not raw:
      print('{,}')
      return it
    return '{,}'

  orig_bytearray = False
  if isinstance(it, bytearray):
    orig_bytearray = True
    it = [hex(x) for x in it]

  orig_bytes = False
  if isinstance(it, bytes):
    orig_bytes = True
    it = [chr(x) for x in it]

  if isinstance(it, dict):
    text = '{'
    for key, value in it.items():
      if recursive and isinstance(value, list | tuple | dict):
        value = print_iterable(value, raw=True).replace('\n', '\n  ')
      else:
        value = repr(value)
      text += f'\n  {key!r}: {value},'
    text += '\n}'
  else:
    text = '[' if isinstance(it, list) else ('{' if isinstance(it, set) else '(')
    for value in it:
      if recursive and isinstance(value, list | tuple | dict):
        value = print_iterable(value, raw=True).replace('\n', '\n  ')
      else:
        if orig_bytearray:
          value = value
        elif orig_bytes:
          value = f'b{value!r}'
        else:
          value = repr(value)
      text += f'\n  {value},'
    text += '\n]' if isinstance(it, list) else ('\n}' if isinstance(it, set) else '\n)')

  if raw:
    return text
  print(text)
  return it
