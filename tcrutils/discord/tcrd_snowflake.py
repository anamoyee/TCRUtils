from ..src.tcr_print import fmt_iterable


class Snowflake(int):
  """Snowflake is an integer in `range((1 << 64) - 1)`."""

  def __tcr_display__(self, **kwargs):
    return fmt_iterable(int(self), **kwargs)


def is_snowflake(snowflake: Snowflake | int | str, *, allow_string=True) -> bool:
  if not isinstance(snowflake, ((int | str) if allow_string else int)):
    return False

  if not str(snowflake).isnumeric() or (int(snowflake) not in range((1 << 64) - 1)):
    return False

  return True
