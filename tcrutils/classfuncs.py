from typing import Any

from .iterable import getattr_queue


def get_classname(obj: Any, *, default: str = "UnknownClass") -> str:
	return getattr_queue(obj, "__class__.__name__", default=default)


def get_name_classname(obj: Any, *, default: str = "UnknownClass") -> str:
	return getattr_queue(obj, "__name__", "__class__.__name__", default=default)


def get_qualname_classname(obj: Any, *, default: str = "UnknownClass") -> str:
	return getattr_queue(obj, "__qualname__", "__name__", "__class__.__name__", default=default)
