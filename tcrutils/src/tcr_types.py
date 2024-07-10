import datetime as dt
from functools import partial

from . import tcr_print as _m_print
from .tcr_int import hex


class QuotelessString(str):
  """Used in tcr.fmt_iterable() in order to format it as a plain text, rather than as `"normal str"`."""


class HexInt(int):
  leading_zeroes: int

  def __new__(cls, value, leading_zeroes=None, **kwargs):
    return super().__new__(cls, value, **kwargs)

  def __init__(self, value, *, leading_zeroes=6, **_):
    self.leading_zeroes = leading_zeroes
    super().__init__()

  def __tcr_fmt__(self, fmt_iterable, **kwargs):
    return fmt_iterable(int(self), **{**kwargs, 'int_formatter': partial(hex, leading_zeroes=self.leading_zeroes)})


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

    return f'{lhs} {rhs}'

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
