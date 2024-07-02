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
    lhs = fmt_iterable(dt.datetime.fromtimestamp(self, tz=self.tz), **kwargs)
    rhs = fmt_iterable([int(self)], **kwargs)

    return f'{lhs} {rhs}'
