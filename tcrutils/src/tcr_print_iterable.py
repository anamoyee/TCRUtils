from collections.abc import Generator, Iterable
from copy import deepcopy as copy
from typing import TypeAlias

from .tcr_color import c
from .tcr_null import Null
from .tcr_other import hex

PIRepassable: TypeAlias = list | tuple | dict | set | Generator | range | bytes | bytearray | str | None | bool

BRACKET_COLOR    = "Cyan"

COLON_COLOR      = "Orange\\_1"
COMMA_COLOR      = "Dark\\_gray"

B_COLOR          = "Red" # b''

TRUE_COLOR       = "Green"
FALSE_COLOR      = "Red"

NULL_COLOR       = "Dark\\_gray"
NONE_COLOR       = "Light\\_gray"

MORE_ITEMS_COLOR = "Purple\\_1B"

def print_iterable(
  it: Iterable,
  *its: Iterable,
  recursive=True,
  raw=False,
  item_limit=100,
  syntax_highlighting=True
) -> str | None:
  """Print an iterable in a nicely formatted way. If raw=True return the nicely formatted string instead of printing.

  Supports lists, tuples, sets, dicts, strings, generators, bytestrings, bytearrays and may work with other Iterables
  `item_limit` determines the limit of iterable items before it displays them instead of continuing to get more
  `syntax_highlighting` adds ansi codes to highlight syntax (may be buggy)
  """

  if its: return print_iterable((it, *its), recursive=recursive, raw=raw, item_limit=item_limit, syntax_highlighting=syntax_highlighting)

  def synhi_s(symbol):
    if not syntax_highlighting: return symbol
    # fmt: off
    colors = {
      ":": COLON_COLOR,
      ",": COMMA_COLOR,
      "[": BRACKET_COLOR,
      "]": BRACKET_COLOR,
      "{": BRACKET_COLOR,
      "}": BRACKET_COLOR,
      "(": BRACKET_COLOR,
      ")": BRACKET_COLOR,
      "<": BRACKET_COLOR,
      ">": BRACKET_COLOR,
      "b": B_COLOR,
    }
    # fmt: on

    return c(colors[symbol]) + symbol + c('reset')

  def synhi(ncstr, origitem: type) -> str:
    # fmt: off
    colors = {
      "str+": 'White',
      "str":  'gold',
      "int":  'Blue'
    }
    # fmt: on


    # input(f"> {ncstr!r} // {origitem!r} ({type(origitem)}) <")
    if not syntax_highlighting: return ncstr
    if origitem == "more":
      return c(MORE_ITEMS_COLOR) + ncstr + c('reset')
    elif origitem is Null:
      return "Null" if not syntax_highlighting else c(NULL_COLOR) + "Null" + c('reset')
    elif origitem is None:
      return "None" if not syntax_highlighting else c(NONE_COLOR) + "None" + c('reset')
    elif origitem is True:
      return "True" if not syntax_highlighting else c(TRUE_COLOR) + "True" + c('reset')
    elif origitem is False:
      return "False" if not syntax_highlighting else c(FALSE_COLOR) + "False" + c('reset')
    elif isinstance(origitem, str):
      return f"{c(colors['str+'])}{ncstr[0]}{c('reset')+c(colors['str'])}{ncstr[1:-1]}{c('reset')}{c(colors['str+'])}{ncstr[-1]}{c('reset')}"
    elif isinstance(origitem, int):
      return f"{c(colors['int'])}{ncstr}{c('reset')}"
    elif isinstance(origitem, bytes):
      return f"{synhi_s('b')}{c(colors['str+'])}{ncstr[1]}{c('reset')+c(colors['str'])}{ncstr[2:-1]}{c('reset')}{c(colors['str+'])}{ncstr[-1]}{c('reset')}"

    return ncstr

  if it is Null:
    return "Null" if not syntax_highlighting else c(NULL_COLOR) + "Null" + c('reset')

  if it is None:
    return "None" if not syntax_highlighting else c(NONE_COLOR) + "None" + c('reset')

  if it is True:
    return "True" if not syntax_highlighting else c(TRUE_COLOR) + "True" + c('reset')

  if it is False:
    return "False" if not syntax_highlighting else c(FALSE_COLOR) + "False" + c('reset')

  if isinstance(it, str):
    it = repr(it)
    if syntax_highlighting: it = synhi(it, '')
    return it if raw else print(it)

  if isinstance(it, bytes):
    it = repr(it)
    if syntax_highlighting: it = synhi(it, b'')
    return it if raw else print(it)

  if it == []:
    if not raw:
      print(f'{synhi_s("[")}{synhi_s("]")}')
      return it
    return f'{synhi_s("[")}{synhi_s("]")}'

  if it == ():
    if not raw:
      print(f'{synhi_s("(")}{synhi_s(")")}')
      return it
    return f'{synhi_s("(")}{synhi_s(")")}'

  if it == {}:
    if not raw:
      print(f'{synhi_s("{")}{synhi_s("}")}')
      return it
    return f'{synhi_s("{")}{synhi_s("}")}'

  if it == set():
    if not raw:
      print(f'{synhi_s("{")}{synhi_s(",")}{synhi_s("}")}')
      return it
    return f'{synhi_s("{")}{synhi_s(",")}{synhi_s("}")}'

  orig_bytearray = False
  if isinstance(it, bytearray):
    orig_bytearray = True
    it = [synhi(hex(x), 1) for x in it]

  orig_bytes = False
  if isinstance(it, bytes):
    orig_bytes = True
    it = [chr(x) for x in it]

  def parenthesis(it: Iterable):
    # fmt: off
    parenthesis_lookup = {
      Generator: ('<', '>'),
      range:     ('<', '>'),
      list:      ('[', ']'),
      set:       ('{', '}'),
      dict:      ('{', '}'),
      tuple:     ('(', ')'),
      None:      ('(', ')'),
    }
    # fmt: on

    default = parenthesis_lookup.pop(None)

    for k, v in parenthesis_lookup.items():
      if isinstance(it, k):
        return tuple(synhi_s(x) for x in v)

    return default

  parenthesis = parenthesis(it)

  if isinstance(it, dict):
    text = parenthesis[0]
    for key, value in it.items():
      ovalu = copy(value)
      if recursive and isinstance(value, PIRepassable):
        value = print_iterable(value, raw=True, item_limit=item_limit, recursive=True, syntax_highlighting=syntax_highlighting).replace('\n', '\n  ')
      elif orig_bytearray:
        value = value
      elif orig_bytes:
        value = synhi(value, b'')
      else:
        value = synhi(repr(value), ovalu)
      text += f'\n  {synhi(repr(key), key)}{synhi_s(":")} {value}{synhi_s(",")}'
    text += f'\n{parenthesis[1]}'
  else:
    text = parenthesis[0]
    vals = 0
    addmore = True
    for value in it:
      if item_limit is not None and item_limit != -1 and vals >= item_limit:
        break
      vals += 1
      ovalu = copy(value)
      if recursive and isinstance(value, PIRepassable) and not orig_bytearray and not orig_bytes:
        value = print_iterable(value, raw=True, item_limit=item_limit, recursive=True, syntax_highlighting=syntax_highlighting).replace('\n', '\n  ')
      else:
        if orig_bytearray:
          pass
        elif orig_bytes:
          value = f'{synhi_s("b")}{value!r}'
        else:
          value = synhi(repr(value), ovalu)
      text += f'\n  {value}{synhi_s(",")}'
    else:
      addmore = False
    if addmore:
      try:
        ns = len(it)-item_limit
      except TypeError:
        ns = '?'
      text += f'\n  {synhi("(", "more")}{synhi(ns, 1)}{synhi(" more items...)", "more")}'
    text += f'\n{parenthesis[1]}'

  if raw:
    return text
  print(text)
  return it
