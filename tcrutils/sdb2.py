import pathlib as p
import shelve
from abc import ABC, abstractmethod


class ShelfManager[T](ABC):
	PATH: p.Path
	OPEN_CONTEXT_TS: dict[str, T] = {}
	OPEN_CONTEXT_AMOUNTS: dict[str, int] = {}

	key: str

	def __init__(self, key: str):
		self.key = str(key)

	@abstractmethod
	def default_factory(self) -> T: ...

	@classmethod
	def open_shelf(cls) -> shelve.Shelf[T]:
		cls.PATH.parent.mkdir(exist_ok=True, parents=True)

		return shelve.open(cls.PATH)  # noqa: SIM115

	@classmethod
	def contains(cls, key: str) -> bool:
		with cls.open_shelf() as shelf:
			return str(key) in shelf

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

		if self.key in self.OPEN_CONTEXT_TS:
			self._current_item = self.OPEN_CONTEXT_TS[self.key]
		else:
			self._current_item = self._shelf[self.key] if self.key in self._shelf else self.default_factory()
			self.OPEN_CONTEXT_TS[self.key] = self._current_item

		self.OPEN_CONTEXT_AMOUNTS.setdefault(self.key, 0)
		self.OPEN_CONTEXT_AMOUNTS[self.key] += 1

		return self._current_item

	def __exit__(self, ty, e: BaseException | None, tb) -> None:
		if e is None:
			self._shelf[self.key] = self._current_item

		if self.OPEN_CONTEXT_AMOUNTS[self.key] == 1:
			del self.OPEN_CONTEXT_TS[self.key]
			del self.OPEN_CONTEXT_AMOUNTS[self.key]
		else:
			self.OPEN_CONTEXT_AMOUNTS[self.key] -= 1

		del self._current_item

		self._shelf.close()
		del self._shelf

	@classmethod
	def delitem_unchecked(cls, key: str) -> None:
		with cls.open_shelf() as shelf:
			del shelf[str(key)]


class SingleShelfManager[T](ShelfManager[T]):
	def __init__(self):
		super().__init__(0)
