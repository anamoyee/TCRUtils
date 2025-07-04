from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from enum import Enum, auto
from functools import wraps
from typing import Any, Generic, Literal, Self, TypeVar, overload

from .print import FMT_BRACKETS


class EmptyType(Enum):
	EMPTY = auto()


Default = TypeVar("Default")


class ResultUnwrappedOnErrorError(Exception):
	"""An unwrap() was called on a Result containing an error."""


class ResultUnwrappedErrOnValueError(Exception):
	"""An unwrap_err() was called on a Result contaning a value."""


class _ResultBase[Ok, Err: BaseException]:
	_value: Ok | Err
	_is_err: bool

	@overload
	def __init__(self, *, is_error: Literal[False], value: Ok): ...

	@overload
	def __init__(self, *, is_error: Literal[True], value: Err): ...

	def __init__(
		self,
		*,
		is_error: bool = False,
		value: Ok | Err,
	):
		self._is_err = bool(is_error)

		if is_error and not isinstance(value, BaseException):
			raise ValueError(f"If is_error=True, value must be an {'**INSTANCE**' if isinstance(value, type) else 'instance'} of a subclass of BaseException")

		self._value = value

	@classmethod
	def new_ok(cls, value: Ok):
		return cls(is_error=False, value=value)

	@classmethod
	def new_err(cls, error: Err):
		return cls(is_error=True, value=error)

	@property
	def is_ok(self) -> bool:
		return not self._is_err

	@property
	def is_err(self) -> bool:
		return self._is_err

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented

		return self._is_err == other._is_err and self._value == other._value

	def unwrap_err(self) -> Err:
		"""If the result contains a value, raise `ResultUnwrappedErrOnValueError()`, else return the error."""
		if not self._is_err:
			raise ResultUnwrappedErrOnValueError() from self._value

		return self._value

	def unwrap_or(self, default: Default) -> Ok | Default:
		"""If the result contains an error, return default, else return the value."""
		if self.is_err:
			return default

		return self._value

	def unwrap_err_or(self, default: Default) -> Err | Default:
		"""If the result contains a value, return default, else return the error."""
		if not self.is_err:
			return default

		return self._value

	def unwrap_or_else(self, default_factory: Callable[[Err], Default]) -> Ok | Default:
		"""If the result contains an error, return `default_factory(that_error)`, else return the value."""
		if self.is_err:
			return default_factory(self._value)

		return self._value

	def unwrap_err_or_else(self, default_factory: Callable[[Ok], Default]) -> Err | Default:
		"""If the result contains a value, return `default_factory(that_value)`, else return the error."""
		if not self.is_err:
			return default_factory(self._value)

		return self._value

	def raise_if_possible(self) -> None:
		"""If the result contains a value, do nothing, otherwise raise the error."""

		if self.is_err:
			raise self._value

	def map_err(self, f: Callable[[Err], Err]) -> Self:
		"""If the result contains an error, set it to `f(current_error)`, else do nothing."""
		if self.is_err:
			self._value = f(self._value)

		return self

	def map_ok(self, f: Callable[[Ok], Ok]) -> Self:
		"""If the result contains a value (Ok), set it to `f(current_value)`, else do nothing."""
		if self.is_ok:
			self._value = f(self._value)

		return self

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		return (
			fmt_iterable(self.__class__)
			+ fmt_iterable(696969.696969).replace("696969", "")
			+ fmt_iterable(bool(self.is_ok)).replace("True", "Ok").replace("False", "Err")
			+ (FMT_BRACKETS[tuple][syntax_highlighting] % fmt_iterable(self._value))
		)

	def unwrap_direct(self) -> Ok:
		"""If the result contains an error, raise it, else return the value."""
		if self._is_err:
			raise self._value

		return self._value

	def unwrap_indirect(self) -> Ok:
		"""If the result contains an error, raise `ResultUnwrappedOnErrorError()`, else return the value."""
		if self._is_err:
			raise ResultUnwrappedOnErrorError() from self._value

		return self._value


class Result[Ok, Err: BaseException](_ResultBase[Ok, Err]):
	"""May contain a value or an error, but not both. Check with `.is_ok` or `.unwrap()`, etc."""

	def unwrap(self) -> Ok:
		"""If the result contains an error, raise `ResultUnwrappedOnErrorError()`, else return the value (On `Result` alias to `.unwrap_indirect()`)."""
		return self.unwrap_indirect()


class Result2[Ok, Err: BaseException](Result[Ok, Err]):
	"""Like Result, but .unwrap() in the sad case raises the underling error, not `ResultUnwrappedOnErrorError()` (On `Result2` alias to `.unwrap_direct()`). Normal `Result`'s `.unwrap()` can also be accessed via `.unwrap_indirect()`."""

	def unwrap(self) -> Ok:
		"""If the result contains an error, raise it, else return the value."""
		return self.unwrap_direct()


def aresultify[**P, R](f: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, Coroutine[Any, Any, Result[R, Exception]]]:
	@wraps(f)
	async def wrapper(*args, **kwargs):
		try:
			return Result.new_ok(await f(*args, **kwargs))
		except Exception as e:
			return Result.new_err(e)

	return wrapper


def resultify[**P, R](f: Callable[P, R]) -> Callable[P, Result[R, Exception]]:
	@wraps(f)
	def wrapper(*args, **kwargs):
		try:
			return Result.new_ok(f(*args, **kwargs))
		except Exception as e:
			return Result.new_err(e)

	return wrapper


def aresultify2[**P, R](f: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, Coroutine[Any, Any, Result2[R, Exception]]]:
	@wraps(f)
	async def wrapper(*args, **kwargs):
		try:
			return Result2.new_ok(await f(*args, **kwargs))
		except Exception as e:
			return Result2.new_err(e)

	return wrapper


def resultify2[**P, R](f: Callable[P, R]) -> Callable[P, Result2[R, Exception]]:
	@wraps(f)
	def wrapper(*args, **kwargs):
		try:
			return Result2.new_ok(f(*args, **kwargs))
		except Exception as e:
			return Result2.new_err(e)

	return wrapper
