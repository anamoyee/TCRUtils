from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum, auto


class TT(Enum):
  TEXT = auto()
  PAREN_OPEN = auto()
  PAREN_CLOSE = auto()

class Execute:
  placeholders: dict[str, Callable]

  def __init__(self, **placeholders: Callable) -> None:
    self.placeholders = placeholders

  def set_placeholder(self, name: str, func: Callable) -> None:
    self.placeholders[name] = func
