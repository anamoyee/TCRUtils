import os
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from random import randint
from typing import Any, NoReturn

from colored import Back, Fore, Style

from .compare import able
from .console import console
from .extract_error import extract_error
from .iterable import getattr_queue
from .print import FMT_BRACKETS, FMTC, fmt_iterable
from .types import UnreprableString
from .void import raiser

ASSERTION_ASS = f"{Style.reset}{Fore.GREEN + Style.bold} PASS {Style.reset}"
"""Uh i meant assertion_pass..."""
ASSERTION_FAIL = f"{Style.reset}{Fore.RED + Style.bold} FAIL {Style.reset}"


def default_asshook(obj, result: bool, *, comment: str = "") -> None:
	"""Default assertion hook (hehe)."""

	console(
		obj,
		padding=f" {(ASSERTION_ASS if randint(1, 1000) != 69 else ASSERTION_ASS.replace('PASS', ' ASS')) if result else ASSERTION_FAIL} ",
		printhook=lambda x, **kwargs: print(x + comment, **kwargs),
	)


def total_default_printhook(s: str, failures: int, total: int, *args, **kwargs):
	console(
		f"{s}{' ' if total else f'{Fore.RED}{Style.bold}< no tests registered > '}{Fore.RED if failures else Fore.GREEN}{Style.bold}{failures}{FMTC.DECIMAL}/{FMTC.NUMBER}{total}{FMTC._}",
		*args,
		fmt_iterable=lambda a, *_, **__: str(a),
		**kwargs,
	)


@dataclass
class _TestResult:
	result: bool


class _Ass:
	_totals: list[_TestResult]
	error_func: Callable[[Exception, str], None]

	EXPR_EQ_BY_FMT = "fmt_iterable(a, syntax_highlighting=True) == fmt_iterable(b, syntax_highlighting=True)"

	def __init__(self, error_func: Callable[[Exception, str], None] | None = None) -> None:
		self._totals = []
		self.error_func = error_func

	def __call__(
		self,
		a: Any,
		b: Any | bool = True,
		/,
		*,
		expr: str = "a == b",
		assert_first: bool = False,
		msg: str | Callable[[Any], Any] = "Assholertion failed",
		printhook: Callable[[Any, bool], None] = default_asshook,
		suppress: bool = False,
		fmt_iterable_kwrags: dict[str, Any] | None = None,
		**printhook_kwargs: Any,
	) -> None:
		"""### assert with tcr.console.

		# WARNING: this is meant for testing only and uses eval().
		# Do not use in any serious code.
		Also.. imagine showing someone some code and it says 'ass' in it so don't use it for that reason too...

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
			fmt_iterable_kwrags = {"syntax_highlighting": True}

		SH = bool(fmt_iterable_kwrags.get("syntax_highlighting"))

		C_TEXT = "" if not SH else FMTC.ITER_I
		C_RESET = "" if not SH else FMTC._
		C_FUNC = "" if not SH else FMTC.FUNCTION
		C_EXC = "" if not SH else FMTC.INTERNAL_EXCEPTION
		comment = ""

		try:
			result = eval(expr) if isinstance(expr, str) else ((expr(a) == expr(b)) if callable(expr) else raiser(TypeError("Invalid typeof expr: " + str(type(expr))))())
		except Exception as e:
			_revcode = "\x1b[7m"
			comment = f" {C_EXC}{_revcode} {extract_error(e)} {C_RESET}"
			result = False
		finally:
			self._totals.append(_TestResult(result))

		if comment:
			pass
		elif result:
			comment = ""
		elif expr == "a == b" or (able(isinstance, b, expr) and isinstance(b, expr)):
			comment = f" {C_TEXT}({C_RESET}{fmt_iterable(b, **fmt_iterable_kwrags)}{C_TEXT} expected){C_RESET}"
		elif callable(expr):
			comment = f" {C_TEXT}({C_RESET}{C_FUNC}{getattr_queue(expr, '__name__', '__class__.__name__', '__qualname__', default='unknown_callable')}{C_RESET}{FMT_BRACKETS[tuple][SH] % fmt_iterable(b, **fmt_iterable_kwrags)}{C_TEXT} expected){C_RESET}"
		elif isinstance(expr, str):
			comment = f" {C_TEXT}({fmt_iterable(expr, **fmt_iterable_kwrags)}{C_TEXT} expected){C_RESET}"

		printhook_partial = partial(printhook, a, result, comment=comment, **printhook_kwargs)

		if not assert_first:
			printhook_partial()
		if not suppress:
			if callable(self.error_func):
				self.error_func(result, msg)
			else:
				assert result, msg
		if assert_first:
			printhook_partial()

	def total(
		self,
		*,
		prefix: str = "",
		ignore_empty: bool = True,
		printhook: Callable[[str, int, int], None] = total_default_printhook,
		flush: bool = True,
		exit_on_fail: bool = True,
		exit_func: Callable[[int], NoReturn] = os._exit,
	) -> None:
		total = len(self._totals)

		if ignore_empty and not total:
			return

		results1 = [r.result for r in self._totals]
		failures = results1.count(False)
		results = [f"{Fore.GREEN + Style.bold}." if x else f"{Fore.RED + Style.bold}X" for x in results1]
		results = "".join(results) + Style.RESET

		print(prefix, end="")
		printhook(results, failures, total)

		if flush:
			self._totals.clear()

		if exit_on_fail and not all(results1):
			print(extract_error(AssertionError(f"Failed {failures} of {total} tests.")))
			exit_func(1)


ass = _Ass()


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
		except Exception:
			...
		return False

	return raises_inner


class _RAss:
	def __call__(self, func: Callable[[], None], *args, **kwargs) -> Callable[[BaseException], None]:
		def rass_inner(__e: BaseException, /) -> None:
			ass(("Yes, raises", __e) if raises(func, *args, **kwargs)(__e) else ("No, does not raise", __e), expr="a[0].startswith('Yes')")

		return rass_inner


rass = _RAss()
