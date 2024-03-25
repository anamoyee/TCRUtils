import datetime
from collections.abc import Callable
from functools import reduce
from sys import exit

from colored import Back, Fore, Style

from .tcr_extract_error import extract_error
from .tcr_getch import getch
from .tcr_print import fmt_iterable
from .tcr_types import QuotelessString


class CC:
  _ = Style.reset
  LOG = Fore.light_green + Style.bold  # 10
  WARN = Fore.YELLOW + Style.bold
  ERROR = Fore.RED + Style.bold
  DEBUG = Fore.purple_1b + Style.bold  # 129
  CRITICAL = Back.RED + Style.bold
  BANG = Fore.WHITE + Back.RED + Style.bold


class Console:
  """### Provides logging capabilities.

  `console(...)` == `console.debug(...)`
  """

  _last_diff: str | None = None

  @staticmethod
  def _get_timestamp():
    return str(datetime.datetime.now())[:-3].replace('.', ',')

  def log(self, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'I {self._get_timestamp()} ') + out
    out = f'{CC.LOG}{out}{CC._}'
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
    out = f'{CC.WARN}{out}{CC._}'
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
    out = f'{CC.ERROR}{out}{CC._}'
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
    diff: bool = False,
    **kwargs,
  ) -> None | object:
    out = fmt_iterable(*[(x if ((not quoteless) or (not isinstance(x, str))) else QuotelessString(x)) for x in (value, *values)], syntax_highlighting=syntax_highlighting, **kwargs)

    prefix = ''
    if withprefix:
      prefix = f'D {self._get_timestamp()}'

    c_debug = ''
    c_reset = ''
    c_bang = ''
    if syntax_highlighting:
      c_debug = CC.DEBUG
      c_reset = CC._
      c_bang = CC.BANG

    def compose(x) -> str:
      return f'{c_debug}{margin}{prefix}{padding}{x}{c_reset}'

    if diff and not self._last_diff:
      printhook(compose('\n' + '\n'.join(['  ' + x for x in out.split('\n')])))
    else:
      if not diff:
        printhook(compose(out))
      else:
        out_lines = out.split('\n')
        last_lines = self._last_diff.split('\n')

        while len(out_lines) < len(last_lines):
          last_lines.pop(-1)

        while len(last_lines) < len(out_lines):
          last_lines.append('')

        diff_out = '\n'.join([
          ('  ' if line == line_old else f'{c_bang}*{c_reset} ') + line for line, line_old in zip(out_lines, last_lines, strict=True)
        ])

        printhook(compose('\n' + diff_out))

    self._last_diff = out
    return None if not passthrough else value

  def critical(self, *values, sep=' ', end='', returnonly=False, withprefix=True) -> None | str:
    if not values:
      values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'C {self._get_timestamp()} ') + out
    out = f'{CC.CRITICAL}{out}{CC._}'
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
    (a := f'{Fore.WHITE + Style.BRIGHT} >>> {Back.RED}BREAKPOINT{Style.RESET_ALL} {Fore.WHITE + Style.BRIGHT}<<<{Style.RESET_ALL}'),
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
