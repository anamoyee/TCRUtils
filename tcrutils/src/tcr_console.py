import datetime
from functools import reduce
from sys import exit

# console was coded before .tcr_color was written
from colored import attr, bg, fg, stylize

from .tcr_color import c
from .tcr_extract_error import extract_error
from .tcr_getch import getch
from .tcr_print_iterable import print_iterable

a = 1 if 1 else 0


class console:
  """### Provides logging capabilities.

  btw `console(...)` == `console.debug(...)`
  """

  @staticmethod
  def _get_timestamp():
    return str(datetime.datetime.now())[:-3].replace('.', ',')

  @classmethod
  def log(cls, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'I {cls._get_timestamp()} ') + out
    out = stylize(out, fg('light_green') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  @classmethod
  def warn(cls, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'W {cls._get_timestamp()} ') + out
    out = stylize(out, fg('yellow') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  @classmethod
  def error(cls, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    values = [(extract_error(x) if isinstance(x, Exception) else x) for x in values]
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'E {cls._get_timestamp()} ') + out
    out = stylize(out, fg('red') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  @classmethod
  def debug(
    cls,
    *values,
    sep=' ',
    end='',
    returnonly=False,
    withprefix=True,
    print_iterable_=True,
    passthrough=True,
    recursive=True,
  ) -> None | str:
    if not values:
      values = ['']
    if len(values) > 1:
      out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    else:
      out = values[0]
    if isinstance(out, type({}.values()) | type({}.keys())):
      out = list(out)
    if print_iterable_ and isinstance(out, list | tuple | dict):
      out = print_iterable(out, raw=True, recursive=recursive)
    out = str(out)
    if withprefix:
      out = (f'D {cls._get_timestamp()} ') + out
    out = stylize(out, fg('magenta') + attr('bold'))  # + attr("underlined"))
    if returnonly:
      return out
    print(out)
    return None if not passthrough else values[0]

  @classmethod
  def critical(cls, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'C {cls._get_timestamp()} ') + out
    out = stylize(out, bg('red') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  def __new__(
    cls,
    *values,
    sep=' ',
    end='',
    returnonly=False,
    withprefix=True,
    print_iterable_=True,
    passthrough=True,
    recursive=True,
  ) -> None | str:
    return console.debug(
      *values,
      sep=sep,
      end=end,
      returnonly=returnonly,
      withprefix=withprefix,
      print_iterable_=print_iterable_,
      passthrough=passthrough,
      recursive=recursive,
    )


def breakpoint(*vals, printhook=console, clear=True, ctrlc=exit) -> None:  # noqa: A001 - That's intentional
  """Stop the program execution until a key is pressed. Optionally pass in things to print."""
  for val in vals:
    printhook(val)
  print(
    (a := f'{c("White")} >>> {c("RED")}BREAKPOINT{c(0)} {c("White")}<<<{c(0)}'),
    end='\r',
  )

  if getch() == b'\x03':
    if clear:
      print(len(a) * ' ', end='')
    ctrlc()
    return

  if clear:
    print(len(a) * ' ', end='\r')
  else:
    print()
  
