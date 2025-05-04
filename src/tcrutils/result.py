from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Generic, Literal, TypeVar, overload

from .print import FMT_BRACKETS


class EmptyType(Enum):
	EMPTY = auto()


Default = TypeVar("Default")


@dataclass
class ResultUnwrappedOnErrorError[Err: BaseException](Exception):
	"""An unwrap() was called on a Result containing an error."""

	that_error: Err


@dataclass
class ResultUnwrappedErrOnValueError[Ok](Exception):
	"""An unwrap_err() was called on a Result contaning a value."""

	that_value: Ok


class Result[Ok, Err: BaseException]:
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

	def unwrap(self) -> Ok:
		"""If the result contains an error, raise ResultUnwrappedIncorrectlyError(that_error), else return the value."""
		if self._is_err:
			raise ResultUnwrappedOnErrorError[Err](self._value)

		return self._value

	def unwrap_err(self) -> Err:
		"""If the result contains a value, raise ResultUnwrappedErrOnValueError(that_value), else return the error."""
		if not self._is_err:
			raise ResultUnwrappedErrOnValueError[Ok](self._value)

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
		"""If the result contains an error, return default_factory(that_error), else return the value."""
		if self.is_err:
			return default_factory(self._value)

		return self._value

	def unwrap_err_or_else(self, default_factory: Callable[[Ok], Default]) -> Err | Default:
		"""If the result contains a value, return default_factory(that_value), else return the error."""
		if not self.is_err:
			return default_factory(self._value)

		return self._value

	def raise_if_possible(self) -> None:
		"""If the result contains a value, do nothing, otherwise raise the error."""

		if self.is_err:
			raise self._value

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		return fmt_iterable(self.__class__) + fmt_iterable(696969.696969).replace("696969", "") + fmt_iterable(bool(self.is_ok)).replace("True", "Ok").replace("False", "Err") + (FMT_BRACKETS[tuple][syntax_highlighting] % fmt_iterable(self._value))
