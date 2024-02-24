import datetime
from collections.abc import Callable
from functools import reduce
from sys import exit

# console was coded before .tcr_color was written
from colored import attr, bg, fg, stylize

from .tcr_color import c
from .tcr_extract_error import extract_error
from .tcr_getch import getch
from .tcr_print import fmt_iterable
from .tcr_types import QuotelessString

a = 1 if 1 else 0


class Console:
  """### Provides logging capabilities.

  `console(...)` == `console.debug(...)`
  """

  @staticmethod
  def _get_timestamp():
    return str(datetime.datetime.now())[:-3].replace('.', ',')

  def log(self, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'I {self._get_timestamp()} ') + out
    out = stylize(out, fg('light_green') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  def warn(self, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'W {self._get_timestamp()} ') + out
    out = stylize(out, fg('yellow') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  def error(self, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    values = [(extract_error(x) if isinstance(x, Exception) else x) for x in values]
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'E {self._get_timestamp()} ') + out
    out = stylize(out, fg('red') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  def debug(
    self,
    value: object,
    /,
    *values: object,
    withprefix: bool = True,
    passthrough: bool = True,
    printhook: Callable[[str], None] = print,
    syntax_highlighting=True,
    margin: str = '',
    padding: str = ' ',
    quoteless: bool = False,
    **kwargs,
  ) -> None | object:
    out = fmt_iterable(*[(x if ((not quoteless) or (not isinstance(x, str))) else QuotelessString(x)) for x in (value, *values)], syntax_highlighting=syntax_highlighting, **kwargs)
    if withprefix:
      out = f'D {self._get_timestamp()}{padding}{out}'
    if syntax_highlighting:
      out = stylize(out, c('Purple\\_1B'))
    printhook(f'{margin}{out}')
    return None if not passthrough else value

  def critical(self, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'C {self._get_timestamp()} ') + out
    out = stylize(out, bg('red') + attr('bold'))
    if returnonly:
      return out
    print(out)
    return None

  def __call__(self, *args, **kwargs) -> None | str:
    return console.debug(*args, **kwargs)

  def __or__(self, other):
    return self.debug(other)

  def __ror__(self, other):
    return self.debug(other)


console = Console()
"""### Provides logging capabilities.

  `console(...)` == `console.debug(...)`
"""


def breakpoint(*vals, printhook=console, clear=True, ctrlc=exit) -> None:
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
