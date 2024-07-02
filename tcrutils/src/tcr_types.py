import datetime as dt

from . import tcr_print as _m_print
from .tcr_int import hex


class QuotelessString(str):
  """Used in tcr.fmt_iterable() in order to format it as a plain text, rather than as `"normal str"`."""


class HexInt(int):
  def __tcr_fmt__(self, fmt_iterable, **kwargs):
    return fmt_iterable(int(self), **{**kwargs, 'int_formatter': hex})


class UnreprableString(QuotelessString):
  def __repr__(self) -> str:
    return self



class UnixTimestampInt(int):
  """Add timezone by assinging the tz attribute after instantiation."""
  def __init__(self, *_, **__) -> None:
    self.tz = None
    super().__init__()

  def __tcr_fmt__(self, fmt_iterable, **kwargs):
    fromtimestamp_value = int(self)

    while fromtimestamp_value > 99_999_999_999: # Convert any milisecond or smaller values to seconds
      fromtimestamp_value //= 1000

    lhs = fmt_iterable(dt.datetime.fromtimestamp(fromtimestamp_value, tz=self.tz), **kwargs)
    rhs = fmt_iterable([int(self)], **kwargs)

    return f'{lhs} {rhs}'
