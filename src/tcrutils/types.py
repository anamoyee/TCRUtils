import datetime as dt
from functools import partial

from .int import hex


class BrainfuckCode(str):
	"""Used in tcr.fmt_iterable() in order to format it as Brainfuck code.

	This will filter out all non-brainfuck characters: `>.<[+-],`.

	This can be used outside of fmt_iterable() to filter characters if needed.
	"""

	def __new__(cls, value):
		return super().__new__(cls, "".join(filter(lambda x: x in ">.<[+-],", value)))


class QuotelessString(str):
	"""Used in tcr.fmt_iterable() in order to format it as a plain text, rather than as `"normal str"`."""


class PlainDisplay[T](tuple[T]):
	def __new__(cls, *iterable: T, sep: str = ""):
		return super().__new__(cls, iterable)

	def __init__(self, *iterable: T, sep: str = ""):
		self.sep = sep
		super().__init__()

	def __tcr_fmt__(self=None, *, fmt_iterable, **_):
		if self is None:
			raise NotImplementedError()

		return self.sep.join(fmt_iterable(x) for x in self)


class LiteralDisplay(str):
	def __tcr_fmt__(self=None, **_):
		if self is None:
			raise NotImplementedError()

		return f"\x1b[0m{self!s}"


class HexInt(int):
	leading_zeroes: int

	def __new__(cls, x, /, *, leading_zeroes=None, prefix=None, **kwargs):
		return super().__new__(cls, x, **kwargs)

	def __init__(self, x, /, *, leading_zeroes=6, prefix="0x", **_):
		self.leading_zeroes = leading_zeroes
		self.prefix = prefix
		super().__init__()

	def __tcr_fmt__(self, fmt_iterable, **kwargs):
		return fmt_iterable(int(self), **{**kwargs, "int_formatter": partial(hex, leading_zeroes=self.leading_zeroes, prefix=self.prefix)})


class UnreprableString(QuotelessString):
	def __repr__(self) -> str:
		return self


class UnixTimestampInt(int):
	"""Add timezone by assinging the tz attribute after instantiation."""

	def __init__(self, *_, **__) -> None:
		self.tz = None
		super().__init__()

	def _get_as_seconds_unix(self) -> int:
		"""Convert this unix timestamp from any type (seconds, miliseconds, microseconds) to the seconds type by dividing by 1000 each time if it's too large to be the seconds variant."""
		i = int(self)

		while i > 99_999_999_999:  # Convert any milisecond or smaller values to seconds
			i //= 1000

		return i

	def __tcr_fmt__(self, fmt_iterable, **kwargs):
		fromtimestamp_value = self._get_as_seconds_unix()

		while fromtimestamp_value > 99_999_999_999:  # Convert any milisecond or smaller values to seconds
			fromtimestamp_value //= 1000

		lhs = fmt_iterable(dt.datetime.fromtimestamp(fromtimestamp_value, tz=self.tz), **kwargs)
		rhs = fmt_iterable([int(self)], **kwargs)

		return f"{lhs} {rhs}"

	def to_datetime(self, tz: dt.tzinfo | None = None) -> dt.datetime:
		"""Evaluate this unix timestamp into a datetime.datetime object."""
		return dt.datetime.fromtimestamp(self._get_as_seconds_unix(), tz=tz)

	def to_int(self):
		"""Forget that this int is a unix timestamp - You may still use this object in place of an int."""
		return int(self)


class GayString(str):
	"""Used in tcr.fmt_iterable() in order to format it as gay str. Happy pride :3"""  # noqa: D400


class AlwaysTruthyStr(str):
	"""A string that always passes an if check no matter the contents."""

	def __bool__(self):
		return True


def _merge_with_common_suffix(*args: str) -> str:
	"""`["OwnedMenu", "UserMenu"] -> "OwnedUserMenu"`."""
	if not args:
		return ""

	common_suffix = ""

	for i in range(1, min(map(len, args)) + 1):
		suffix = args[0][-i:]
		if all(s.endswith(suffix) for s in args):
			common_suffix = suffix
		else:
			break
	else:
		common_suffix = args[0]

	return "".join(s.removesuffix(common_suffix) for s in args) + common_suffix


def DynType(*bases: type) -> type:
	"""Make a dynamic, multiple-inherited type."""
	if not bases:
		raise ValueError("At least one base class must be provided")

	if len(bases) == 1:
		return bases[0]

	name = _merge_with_common_suffix(*(b.__name__ for b in bases if hasattr(b, "__name__"))) or "UnnamedDynType"

	return type(name, bases, {})
