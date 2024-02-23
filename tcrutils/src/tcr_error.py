"""TCRUtils-specific errors."""
from types import TracebackType
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

  class DatabaseError(Exception):
    """Used when database raises an unexpected exception."""

    def __init__(self) -> None:
      super().__init__()

  class NoMatchingOverloadError(Exception):
    """Used in tcr.Overload."""


for attr_name, attr_value in error.__dict__.items():
  if not attr_name.startswith('__'):
    globals()[attr_name] = attr_value

__all__ = [x for x in globals() if not x.startswith('_') and x != error.__name__]
