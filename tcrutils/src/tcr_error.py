"""TCRUtils-specific errors."""
from typing import Any


class error:
  class ConfigurationError(ValueError):
    """Used when a user-provided configuration causes an invalid state."""

  class NotIntegerError(TypeError):
    """Used when integer was expected but not supplied."""
    def __init__(self, not_integer: Any | None = None, /) -> None:
      s = 'Integer was expected.'
      if not_integer:
        s += f" Got '{not_integer!r} instead'"
      super().__init__(s)

for attr_name, attr_value in error.__dict__.items():
    if not attr_name.startswith("__"):
        globals()[attr_name] = attr_value

__all__ = [x for x in globals() if not x.startswith('_') and x != error.__name__]
