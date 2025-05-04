from collections.abc import Awaitable, Callable
from typing import Any, NoReturn


def void(*args: Any, **kwargs: Any) -> None:
	"""Synchronous voider: take any arguments and do nothing, useful in functions that require a callback when nothing is needed to be done."""


async def avoid(*args: Any, **kwargs: Any) -> None:
	"""Asynchronous voider: take any arguments and do nothing, useful in functions that require a callback when nothing is needed to be done."""


def raiser(e: Exception):
	"""With decorator-like structure return a synchronous callable which raises specified exception on call, no matter what (with *args, **kwargs which are ignored)."""

	def inner_raiser(*args, **kwargs) -> NoReturn:
		raise e

	return inner_raiser


async def araiser(e: Exception):
	"""With decorator-like structure return an asynchronous callable which raises specified exception on call, no matter what (with *args, **kwargs which are ignored)."""

	async def inner_raiser(*args, **kwargs) -> NoReturn:
		raise e

	return inner_raiser


def alambda[T, **P](f: Callable[P, T]) -> Callable[P, Awaitable[T]]:
	"""Asyncify any synchronous function, mostly lambdas when needed."""

	async def wrapper(*args, **kwargs):
		return f(*args, **kwargs)

	return wrapper

@lambda x: x()
class Void:
	def __call__(self, *args: Any, **kwargs: Any):
		return self

	def __getattr__(self, name):
		return self

	def __bool__(self):
		return False
