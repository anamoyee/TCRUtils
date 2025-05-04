import contextlib
import inspect
import traceback
from collections.abc import Callable
from types import ModuleType

from .compare import able
from .iterable import getattr_queue


def extract_error(e: BaseException, pattern="%s: %s", *, raw=False) -> tuple[str, str] | str:
	if able(issubclass, e, BaseException) and issubclass(e, BaseException):
		tup = (getattr_queue(e, "__name__", "__class__.__name__", default="!UnknownExceptionGroupClass"), "<class>")
		return tup if raw else pattern % tup

	if able(issubclass, e, Exception) and issubclass(e, Exception):
		tup = (getattr_queue(e, "__name__", "__class__.__name__", default="!UnknownExceptionClass"), "<class>")
		return tup if raw else pattern % tup

	if callable(e):
		e = e()

	one = getattr_queue(e, "__name__", "__class__.__name__", default="!UnknownException")
	two = str(e)
	return (one, two) if raw else pattern % (one, two)


def extract_traceback(e: BaseException) -> str:
	traceback_details = traceback.format_tb(e.__traceback__)
	return "".join(traceback_details)


def print_exception_with_traceback(e: BaseException, *, printhook: Callable[[str], None] = print) -> None:
	printhook("Traceback (most recent call last):")
	printhook(extract_traceback(e))
	printhook(extract_error(e))


def module_error_map(module: ModuleType) -> dict[str, BaseException]:
	"""Get all exception classes in a module."""
	return {name: obj for name, obj in vars(module).items() if inspect.isclass(obj) and issubclass(obj, BaseException) and not issubclass(obj, Warning)}


def modules_error_map(*modules: ModuleType) -> dict[str, BaseException]:
	"""Get all exception classes in a list of modules."""
	return {f"{module.__name__}.{name}".removeprefix("builtins."): exc for module in modules for name, exc in module_error_map(module).items()}
