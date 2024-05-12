import datetime
import inspect
from collections.abc import Callable
from functools import reduce
from sys import exit

from colored import Back, Fore, Style

from .tcr_dict import clean_dunder_dict
from .tcr_extract_error import extract_error, extract_traceback
from .tcr_getch import getch
from .tcr_iterable import cut_at
from .tcr_print import FMTC, fmt_iterable
from .tcr_terminal import terminal
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
    fmt_iterable: Callable[..., str] = fmt_iterable,
    **kwargs,
  ) -> None | object:
    out = fmt_iterable(*[(x if ((not quoteless) or (not isinstance(x, str))) else QuotelessString(x)) for x in (value, *values)], syntax_highlighting=syntax_highlighting, **kwargs)

    if padding == ' ' and not withprefix:
      padding = ''

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

        diff_out = '\n'.join([('  ' if line == line_old else f'{c_bang}*{c_reset} ') + line for line, line_old in zip(out_lines, last_lines, strict=True)])

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

  def hr(self, **kwargs):
    self.debug(QuotelessString('=' * (terminal.width)), margin='\n', withprefix=False, **kwargs)

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


def _clean_built_in_methods(d: dict) -> dict:
  return {k: v for k, v in d.items() if not isinstance(v, type(abs))}


def start_eval_session(f_backs: int = 2) -> None:
  """Starts an interactive shell. For debugging purposes."""
  try:
    current_frame = inspect.currentframe()
    for _ in range(f_backs):
      current_frame = current_frame.f_back
    desired_locals = current_frame.f_locals
    desired_globals = current_frame.f_globals

    a = ' '
    while a:
      a = input('\n\r>>> ')
      if a:
        try:
          if a.strip().lower() == 'locals':
            console(_clean_built_in_methods(clean_dunder_dict(desired_locals)))
          elif a.strip().lower() == 'globals':
            console(_clean_built_in_methods(clean_dunder_dict(desired_globals)))
          elif a.strip().lower() == 'code':
            lines, start_line = inspect.findsource(current_frame)
            lineno = current_frame.f_lineno

            AROUND = 2
            CUTOFF = 70

            lines = lines[max(0, lineno - (AROUND + 1)) : lineno + AROUND]
            while all(x.startswith(' ') for x in lines):
              lines = [x[1:] for x in lines]
            lines = [f'{FMTC.NUMBER}{lineno-AROUND+i}{Fore.yellow + Style.bold} {">" if i == AROUND else "|"}{FMTC._} {cut_at(x, CUTOFF)}' for i, x in enumerate(lines)]
            lines = ''.join(lines)

            print(lines)
          else:
            console(eval(a, desired_locals, desired_globals))
        except Exception as e:
          console.error(f'\n\n{extract_traceback(e)}\n{extract_error(e)}')
  except (KeyboardInterrupt, EOFError):
    print('\r' + (' ' * terminal.width) + '\r', end='')
    exit()


def breakpoint(*vals, printhook=console, clear=True, ctrlc: Callable[[], None] = start_eval_session) -> None:
  """Stop the program execution until a key is pressed. Optionally pass in things to print."""
  vals and printhook(*vals)
  print(
    (a := f'{Fore.WHITE + Style.BOLD} >>> {Back.RED}BREAKPOINT{Style.RESET} {Fore.WHITE + Style.BOLD}<<<{Style.RESET}'),
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
