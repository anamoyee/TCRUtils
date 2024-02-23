from collections.abc import Callable
from functools import partial
from random import randint
from typing import Any

from colored import attr, bg, fg

from .tcr_console import console

ASSERTION_ASS = f"{attr(0)}{fg('green')}{attr('bold')} PASS {attr(0)}"
"""Uh i meant assertion_pass..."""
ASSERTION_FAIL = f"{attr(0)}{bg('red')}{attr('bold')} FAIL {attr(0)}"


def default_asshook(obj, result: bool) -> None:
  """Default assertion hook (hehe)."""

  console(obj, padding=f" {(ASSERTION_ASS if randint(1, 100) != 69 else ASSERTION_ASS.replace('PASS', ' ASS')) if result else ASSERTION_FAIL} ")


def asshole(
  a: Any,
  b: Any | bool = True,
  /,
  *,
  expr: str = 'a == b',
  assert_first: bool = False,
  msg: str = 'Assholertion failed',
  printhook: Callable[[Any, bool], None] = default_asshook,
  suppress: bool = False,
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

  result = eval(expr)

  printhook_partial = partial(printhook, a, result, **printhook_kwargs)

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
