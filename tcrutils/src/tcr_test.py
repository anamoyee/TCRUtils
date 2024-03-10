from collections.abc import Callable
from functools import partial
from random import randint
from typing import Any

from colored import Back, Fore, Style

from .tcr_compare import able
from .tcr_console import console
from .tcr_extract_error import extract_error
from .tcr_iterable import getattr_queue
from .tcr_print import FMT_BRACKETS, FMTC, fmt_iterable
from .tcr_void import raiser

ASSERTION_ASS = f"{Style.reset}{Fore.GREEN + Style.bold} PASS {Style.reset}"
"""Uh i meant assertion_pass..."""
ASSERTION_FAIL = f"{Style.reset}{Fore.RED + Style.bold} FAIL {Style.reset}"


def default_asshook(obj, result: bool, *, comment: str = '') -> None:
  """Default assertion hook (hehe)."""

  console(
    obj,
    padding=f" {(ASSERTION_ASS if randint(1, 100) != 69 else ASSERTION_ASS.replace('PASS', ' ASS')) if result else ASSERTION_FAIL} ",
    printhook=lambda x, **kwargs: print(x + comment, **kwargs),
  )


def asshole(
  a: Any,
  b: Any | bool = True,
  /,
  *,
  expr: str = 'a == b',
  assert_first: bool = False,
  msg: str | Callable[[Any], Any] = 'Assholertion failed',
  printhook: Callable[[Any, bool], None] = default_asshook,
  suppress: bool = False,
  fmt_iterable_kwrags: dict[str, Any] | None = None,
  **printhook_kwargs: Any,
) -> None:
  """### assert + tcr.console (yes i couldn't find a better name for this one).

  # WARNING: this is meant for testing only and uses eval().
  # Do not use in any serious code.
  Also.. imagine showing someone some code and it says 'asshole' in it so don't use it for that reason too...

  This uses the assert keyword so it will be optimized out when using optimization flags.

  Args:
      a: Any, item tested, the one printed
      b: Any, tiem expected, not printed, only tested against
      expr: str, the expression used to test a and b (default: 'a == b')
      assert_first: bool, whether or not to assert first then print (default: False)
      msg: str, the message passed to assertion error, if it happens to be raised
      printhook: Callable[[Any, bool], None], the function to be used for printing the object, first argument: the object, second argument: assertion result (default: tcr.console-ish printer)
      suppress: bool, whether or not to suppress the assertion error and only use the printing functions (default: False)
  """
  if fmt_iterable_kwrags is None:
    fmt_iterable_kwrags = {'syntax_highlighting': True}

  SH = bool(fmt_iterable_kwrags.get('syntax_highlighting'))

  C_TEXT = '' if not SH else FMTC.ITER_I
  C_RESET = '' if not SH else FMTC._
  C_FUNC = '' if not SH else FMTC.FUNCTION
  C_EXC = '' if not SH else FMTC.INTERNAL_EXCEPTION
  comment = ''

  try:
    result = eval(expr) if isinstance(expr, str) else ((expr(a) == expr(b)) if callable(expr) else raiser(TypeError('Invalid typeof expr: ' + str(type(expr))))())
  except Exception as e:
    _revcode = '\x1b[7m'
    comment = f' {C_EXC}{_revcode} {extract_error(e)} {C_RESET}'
    result = False

  if comment:
    pass
  elif result:
    comment = ''
  elif expr == 'a == b' or (able(isinstance, b, expr) and isinstance(b, expr)):
    comment = f' {C_TEXT}({C_RESET}{fmt_iterable(b, **fmt_iterable_kwrags)}{C_TEXT} expected){C_RESET}'
  elif callable(expr):
    comment = f' {C_TEXT}({C_RESET}{C_FUNC}{getattr_queue(expr, '__name__', '__class__.__name__', '__qualname__', default='unknown_callable')}{C_RESET}{FMT_BRACKETS[tuple][SH] % fmt_iterable(b, **fmt_iterable_kwrags)}{C_TEXT} expected){C_RESET}'
  elif isinstance(expr, str):
    comment = f' {C_TEXT}({fmt_iterable(expr, **fmt_iterable_kwrags)}{C_TEXT} expected){C_RESET}'

  printhook_partial = partial(printhook, a, result, comment=comment, **printhook_kwargs)

  if not assert_first:
    printhook_partial()
  if not suppress:
    assert result, msg
  if assert_first:
    printhook_partial()


def raises(func: Callable[[], None], *args, **kwargs) -> Callable[[BaseException], bool]:
  """### Double call: raises(func, args, kwargs=)(exception) -> bool.

  Returns a function that takes an exception which in turn returns the result of whether the func raises that exception as a bool.

  This silences any exceptions raised inside of `func`, only returning True or False based on if that exception is e or not (or if no exception return False)

  ```py
  >>> raises((lambda x: 1 / x), x=1)(ZeroDivisionError)
  False
  >>> raises((lambda x: 1 / x), x=0)(ZeroDivisionError)
  True
  """

  def raises_inner(__e: BaseException, /) -> bool:
    try:
      func(*args, **kwargs)
    except __e:
      return True
    except Exception: ...
    return False

  return raises_inner


def rashole(func: Callable[[], None], *args, **kwargs) -> Callable[[BaseException], None]:
  def rashole_inner(__e: BaseException, /) -> None:
    asshole(('Yes, raises', __e) if raises(func, *args, **kwargs)(__e) else ('No, does not raise', __e), expr="a[0].startswith('Yes')")

  return rashole_inner
