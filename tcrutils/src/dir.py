from builtins import vars as _builtin_vars
from collections.abc import Callable, Iterable
from typing import Any

from .dict import merge_dicts


def vars(x: object, /) -> dict[str, Any]:
	"""Just like builtin vars() but also works on slotted instances (without `__dict__`)."""
	try:
		return _builtin_vars(x)
	except TypeError:
		return {k: getattr(x, k) for k in dir(x)}


def dir2(x: object, /, dir: Callable[[object], Iterable[str]] = dir) -> list[str]:
	"""Same as dir, but exclude the entries starting with '__' (double underscore)."""
	return [y for y in dir(x) if not y.startswith("__")]


def vars2(x: object, /, vars: Callable[[object], dict[str, Any]] = vars) -> dict[str, Any]:
	"""Same as vars, but exclude the keys starting with '__' (double underscore)."""
	return {k: v for k, v in vars(x).items() if not k.startswith("__")}


def dir3(x: object, /, dir: Callable[[object], Iterable[str]] = dir) -> list[str]:
	"""Same as dir, but exclude the entries starting with '_' (single underscore)."""
	return [y for y in dir(x) if not y.startswith("_")]


def vars3(x: object, /, vars: Callable[[object], dict[str, Any]] = vars) -> dict[str, Any]:
	"""Same as vars, but exclude the keys starting with '_' (single underscore)."""
	return {k: v for k, v in vars(x).items() if not k.startswith("_")}


def dir_recursive(x: object, /) -> list[str]:
	"""Checks all attributes recursively and returns a kind of recursive dir(). Also picks up on defaults since it goes all the way down to type/object in mro."""
	return list(vars_recursive(x))


def vars_recursive(x: object, /) -> dict[str, Any]:
	"""Checks all attributes recursively and returns a kind of recursive vars(). Also picks up on defaults since it goes all the way down to type/object in mro."""
	return merge_dicts(x.__dict__, *[o.__dict__ for o in x.__class__.__mro__], {})
