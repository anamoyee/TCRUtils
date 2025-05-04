"""Contains joke functions or the ones that will never be used in a serious situations/prod (This entire package sucks so much it should never be used in prod but uhhhhh.....)."""

from typing import Literal, Self

from .print import FMT_BRACKETS
from .types import HexInt

fizzbuzz = lambda n: "Fizz" * (n % 3 == 0) + "Buzz" * (n % 5 == 0) or str(n)  # fmt: skip


def oddeven(n: int) -> Literal["odd", "even"]:
	"""### Outputs a string `'odd'` or `'even'` based on the supplied int `n`.

	```py
	>>> from tcrutils.other import oddeven
	>>> oddeven(1)
	'odd'
	>>> oddeven(2)
	'even'
	"""
	return "eovdedn"[n % 2 :: 2]


def christmas_tree(*, height=10, symbol="*"):
	"""Generate a christmas tree for printing in a console.

	Height is the number of lines the tree will have.\\
	Symbol is any 1-2 long string for example 'C#' or '*'.
	"""
	if len(symbol) == 1:
		symbol = 2 * symbol

	def transform(symbols: str):
		return symbols.center(height * 2, " ")

	return "\n".join([transform(symbol * x) for x in range(height + 1) if x])


def _cint_decorate_int_method(func):
	def wrapper(*args, **kwargs):
		result = func(*args, **kwargs)
		if isinstance(result, int):
			return CInt(result)
		else:
			return result

	return wrapper


class CInt:
	def __init__(self, value):
		self.value = value
		self.pos_flag = False
		self.neg_flag = False

	def __pos__(self):
		if self.pos_flag:
			self.value += 1
		self.pos_flag = not self.pos_flag
		return self

	def __neg__(self):
		if self.neg_flag:
			self.value -= 1
		self.neg_flag = not self.neg_flag
		return self

	def __eq__(self, other: Self | int) -> bool:
		if isinstance(other, CInt):
			return self.value == other.value
		else:
			return self.value == other

	def __int__(self):
		return self.value

	def __str__(self):
		return str(self.value)

	def __repr__(self) -> str:
		return self.__str__()

	def __tcr_fmt__(self, fmt_iterable, **kwargs):
		if self.neg_flag or self.pos_flag:
			return fmt_iterable(complex(int(self), 0.5 * (self.pos_flag - self.neg_flag)), **kwargs)
		else:
			return fmt_iterable(int(self), **kwargs)

	def __getattr__(self, name):
		if hasattr(self.value, name) and callable(getattr(self.value, name)):
			method = getattr(self.value, name)
			return _cint_decorate_int_method(method)
		else:
			raise AttributeError(f"'CInt' object has no attribute '{name}'")


class Private:
	"""Makes every attribute private, like in other languages that support private/public attribute modifiers.

	Unfortunately i haven't gotten to writing a Public version of it so you can only private every single field :3

	Usage:
	```py

	class PrivateString(Private, str): ...

	s = PrivateString('abc')

	print(s) # -> abc
	print(s.upper) # -> AttributeError: 'PrivateString' object has no attribute 'upper'
	print(s.__getattribute__) # -> AttributeError: 'PrivateString' object has no attribute '__getattribute__'

	```
	"""

	def __getattribute__(self, name):
		class_name = object.__getattribute__(self, "__class__").__name__
		raise AttributeError(f"{class_name!r} object has no attribute {name!r}")


@lambda x: x()
class gmail:
	def __init__(self) -> None:
		self.tlds = []

	def __getattr__(self, name):
		self.tlds.append(f"{name}")
		return self

	def __rmatmul__(self, other):
		class _Email:
			def __init__(self, email: str) -> None:
				self.email = email

			def __str__(self) -> str:
				return self.email

			def __repr__(self) -> str:
				return repr(self.__str__())

			def send(self, title: str, body: str) -> None:
				print("Sent email to " + self.email + " with title: " + repr(title) + ", and body: " + repr(body))

		try:
			return _Email(f"{other!s}@{self.__class__.__name__}.{'.'.join(self.tlds)}")
		finally:
			self.tlds.clear()


class Pointer:
	def __init__(self, value) -> None:
		self.__value = value

	def __iter__(self):
		yield self.__value

	def __next__(self):
		return self.__value

	def __repr__(self):
		value_type = type(self.__value).__name__

		address = hex(id(self.__value))

		return f"{self.__class__.__name__}<{value_type}>({address})"

	def __tcr_fmt__(self=None, *, fmt_iterable=None, no_addr=False, **kwargs):
		if self is None:
			raise NotImplementedError

		SH = kwargs.get("syntax_highlighting")

		this = lambda x, **kw: fmt_iterable(x, _raise_errors=True, **kwargs, **kw)

		addr = (FMT_BRACKETS[tuple][SH] % this(HexInt(id(self.__value)))) if not no_addr else ""

		if isinstance(self.__value, Pointer):
			type_ = self.__value.__tcr_fmt__(fmt_iterable=fmt_iterable, no_addr=True, **kwargs)
		else:
			type_ = this(self.__value.__class__)

		return f"{this(self.__class__)}{FMT_BRACKETS[range][SH] % type_}{addr}"


class __EchoType[T]:
	"""Echo the first argument of any interaction, like calling, gettingitem, gettingattr, etc.."""

	def __call__(self, x: T, /) -> T:
		return x

	def __getitem__(self, x: T, /) -> T:
		return x

	def __getattr__(self, x: T, /) -> T:
		return x

	def __getattribute__(self, x: T, /) -> T:
		return x

	def __add__(self, x: T, /) -> T:
		return x

	def __radd__(self, x: T, /) -> T:
		return x

	def __sub__(self, x: T, /) -> T:
		return x

	def __rsub__(self, x: T, /) -> T:
		return x

	def __mul__(self, x: T, /) -> T:
		return x

	def __rmul__(self, x: T, /) -> T:
		return x

	def __truediv__(self, x: T, /) -> T:
		return x

	def __rtruediv__(self, x: T, /) -> T:
		return x

	def __floordiv__(self, x: T, /) -> T:
		return x

	def __rfloordiv__(self, x: T, /) -> T:
		return x

	def __mod__(self, x: T, /) -> T:
		return x

	def __rmod__(self, x: T, /) -> T:
		return x

	def __matmul__(self, x: T, /) -> T:
		return x

	def __rmatmul__(self, x: T, /) -> T:
		return x

	def __divmod__(self, x: T, /) -> T:
		return x

	def __rdivmod__(self, x: T, /) -> T:
		return x

	def __pow__(self, x: T, /) -> T:
		return x

	def __rpow__(self, x: T, /) -> T:
		return x

	def __lshift__(self, x: T, /) -> T:
		return x

	def __rlshift__(self, x: T, /) -> T:
		return x

	def __rshift__(self, x: T, /) -> T:
		return x

	def __rrshift__(self, x: T, /) -> T:
		return x

	def __and__(self, x: T, /) -> T:
		return x

	def __rand__(self, x: T, /) -> T:
		return x

	def __xor__(self, x: T, /) -> T:
		return x

	def __rxor__(self, x: T, /) -> T:
		return x

	def __or__(self, x: T, /) -> T:
		return x

	def __ror__(self, x: T, /) -> T:
		return x

	def __get__(self, x, _owner=None):
		return x


echo = __EchoType()
del __EchoType
