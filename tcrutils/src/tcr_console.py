import datetime
import inspect
from collections.abc import Callable
from functools import partial, reduce
from sys import argv, exit

from colored import Back, Fore, Style

from .tcr_decorator import copy_kwargs_sunder
from .tcr_dict import clean_dunder_dict
from .tcr_extract_error import extract_error, extract_traceback
from .tcr_getch import getch
from .tcr_inspect import get_file_colon_lineno
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
  include_callsite: bool = None

  @staticmethod
  def _get_timestamp():
    return str(datetime.datetime.now())[:-3].replace('.', ',')

  def _get_callsite_text_if_enabled(self, backtrack_frames) -> str:
    if self.include_callsite or (self.include_callsite is None and '--tcr-c-callsite' in argv):
      return get_file_colon_lineno(backtrack_frames=backtrack_frames)
    return ''

  @copy_kwargs_sunder
  def _generate_out_and_print(self, *values, sep='\n', end='', withprefix=True, syntax_highlighting: bool = True, color: str, letter: str, _kwargs: dict, **kwargs) -> None:
    if not values:
      values = ('',)

    if len(values) > 1:
      for i, v in enumerate(values):
        if i == 0:
          char = 'V'
        elif i == len(values) - 1:
          char = 'Λ'
        else:
          char = '│'

        print(char, end=' ')

        self._generate_out_and_print(v, **_kwargs)
      return

    values = [
      (x if isinstance(x, str) else fmt_iterable(x, syntax_highlighting=syntax_highlighting, **kwargs))
      for x in values
    ]

    out = sep.join(values)
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end

    if withprefix:
      out = f'{letter} {(self._get_callsite_text_if_enabled(5)+" ").lstrip()}{self._get_timestamp()} ' + out

    out = f'{color if syntax_highlighting else ""}{out}{CC._ if syntax_highlighting else ""}'

    print(out)

  def log(self, *values, sep=' ', end='', withprefix=True) -> None | str:
    self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.LOG, letter='I')

  def warn(self, *values, sep=' ', end='', withprefix=True) -> None | str:
    self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.WARN, letter='W')

  def error(self, *values, sep=' ', end='', withprefix=True) -> None | str:
    self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.ERROR, letter='E')

  def critical(self, *values, sep=' ', end='', withprefix=True) -> None | str:
    self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.CRITICAL, letter='C')

  def debug(
    self,
    value: object = ...,
    /,
    *values: object,
    withprefix: bool = True,
    passthrough: bool = False,
    printhook: Callable[[str], None] = print,
    syntax_highlighting=True,
    margin: str = '',
    padding: str = ' ',
    quoteless: bool = True,
    diff: bool = False,
    fmt_iterable: Callable[..., str] = fmt_iterable,
    **kwargs,
  ) -> None | object:
    out = fmt_iterable(*[(x if ((not quoteless) or (x.__class__ != str)) else QuotelessString(x)) for x in (value, *values)], syntax_highlighting=syntax_highlighting, **kwargs)

    if padding == ' ' and not withprefix:
      padding = ''

    prefix = ''
    if withprefix:
      prefix = f'D {(self._get_callsite_text_if_enabled(4)+" ").lstrip()}{self._get_timestamp()}'

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

  def hr(self, newlines_on_both_sides: bool = True, **kwargs):
    newline = '\n' if newlines_on_both_sides else ''
    self.debug(QuotelessString(newline + ('=' * terminal.width) + newline), withprefix=False, **kwargs)

  def __call__(self, *args, **kwargs) -> None | str:
    return console.debug(*args, **kwargs)

  def __or__(self, other):
    return self.debug(other, passthrough=True)

  def __ror__(self, other):
    return self.debug(other, passthrough=True)


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
