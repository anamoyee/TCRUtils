import pathlib as p
import shelve
from abc import ABC, abstractmethod


class ShelfManager[T](ABC):
	PATH: p.Path

	key: str

	def __init__(self, key: str):
		self.key = str(key)

	@abstractmethod
	def default_factory(self) -> T: ...

	@classmethod
	def open_shelf(cls) -> shelve.Shelf[str, T]:
		cls.PATH.parent.mkdir(exist_ok=True, parents=True)

		return shelve.open(cls.PATH)  # noqa: SIM115

	@classmethod
	def contains(cls, key: str) -> bool:
		with cls.open_shelf() as shelf:
			return key in shelf

	@classmethod
	def keys(cls) -> list[str]:
		with cls.open_shelf() as shelf:
			return list(shelf.keys())

	@classmethod
	def values(cls) -> list[T]:
		with cls.open_shelf() as shelf:
			return list(shelf.values())

	@classmethod
	def items(cls) -> list[tuple[str, T]]:
		with cls.open_shelf() as shelf:
			return list(shelf.items())

	def __enter__(self) -> T:
		self._shelf = self.open_shelf()

		self._current_item = self._shelf[self.key] if self.key in self._shelf else self.default_factory()
		return self._current_item

	def __exit__(self, ty, e: BaseException | None, tb) -> None:
		if e is None:
			self._shelf[self.key] = self._current_item

		del self._current_item

		self._shelf.close()
		del self._shelf


class SingleShelfManager[T](ShelfManager[T]):
	def __init__(self):
		super().__init__(0)
