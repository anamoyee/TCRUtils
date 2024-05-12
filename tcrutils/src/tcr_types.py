from .tcr_int import hex


class QuotelessString(str):
  """Used in tcr.fmt_iterable() in order to format it as a plain text, rather than as `"normal str"`."""


class HexInt(int):
  def __tcr_fmt__(self, fmt_iterable, **kwargs):
    return fmt_iterable(int(self), **{**kwargs, 'int_formatter': hex})


class UnreprableString(QuotelessString):
  def __repr__(self) -> str:
    return self
