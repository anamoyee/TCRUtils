from typing import Any


def void(*args: Any, **kwargs: Any) -> None:
  """Synchronouś voider, takes any arguments and does nothing, useful in functions that require an argument when nothing is needed to be done."""


async def avoid(*args: Any, **kwargs: Any) -> None:
  """Asynchronous voider, takes any arguments and does nothing, useful in functions that require an argument when nothing is needed to be done."""
