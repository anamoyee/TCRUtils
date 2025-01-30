"""Functions related to comparisons, didn't want to name the file tcr_test.py to avoid confusion with testing as in testing if code works."""

from collections.abc import Callable
from typing import Any


class AbleResult:
	"""Contains a result from tcr.able().

	May be used in an if statement or bool(able_result) expression, in whichc ase
	"""

	result: Any | BaseException
	truefalse: bool
	"""Can't name it bool, can't name it result, can't name it anything... bruh. truefalse it is then"""

	def __init__(self, truefalse: bool, result: Any):
		self.truefalse = truefalse
		self.result = result

	def __bool__(self) -> bool:
		return self.truefalse

	def __iter__(self):
		yield self.truefalse
		yield self.result


def able(func: Callable, *args, able_exception__: BaseException = Exception, **kwargs) -> AbleResult:
	"""### Return True* if x is func(x)-able aka does not raise any errors while passed in to func otherwise return False*.

	*The result type is AbleResult, not bool, but it's bool-able (can be used in an if statement or bool(able_result) normally)

	#### Example:
	```py
	>>> able(int, '1') # Wouldn't raise any Exception
	True
	>>> able(int, 'a') # Would raise: ValueError: invalid literal for int() with base 10: 'a'
	False
	>>> [int(x) for x in [] if able(int, x)]
	```

	#### Result retrieving example:
	```py
	>>> color = 'ff8000' # a hex encoded color code
	>>> if (r := able(int, color, base=16)):
	...   print(repr(r.result))
	16744448
	>>> color = 'ff8000'
	>>> if (r := able(int, color)) or True: # oops! forgot to set the base (and added or True so this example actually prints)
	...   print(repr(r.result)) # Returns False along with the exception in the result field
	ValueError("invalid literal for int() with base 10: 'ff8000'")
	```
	"""
	try:
		result = func(*args, **kwargs)
	except able_exception__ as e:
		return AbleResult(False, e)
	else:
		return AbleResult(True, result)


def able_simple[**P](f: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> bool:
	try:
		f(*args, **kwargs)
	except Exception:
		return False
	else:
		return True


def able_simple_result[**P, R](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> None | R:
	try:
		result = f(*args, **kwargs)
	except Exception:
		return False
	else:
		return result


def isdunder(s: str):
	"""Return True if the string ends and starts with at least two underscores each.

	A 2-char string containing just underscores is considered dunder.
	"""

	return s.startswith("__") and (s.endswith("__"))
