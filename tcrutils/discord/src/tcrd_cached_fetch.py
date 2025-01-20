from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

Output = TypeVar("Output")
ConvertedOutput = TypeVar("ConvertedOutput")
Call = TypeVar("Call", bound=Callable[[], Coroutine[Any, Any, Output]])

_MISSING = object()


class AsyncCachedFetch:
	async_callable: Call
	_last_result: Output = _MISSING

	def __init__(self, async_callable: Call):
		self.async_callable = async_callable

	async def get(self) -> Output:
		if self._last_result is _MISSING:
			self._last_result = await self.fetch()
		return self._last_result

	async def fetch(self) -> Output:
		return await self.async_callable()

	def has_cache(self) -> bool:
		return self._last_result is not _MISSING

	def clear_cache(self) -> None:
		self._last_result = None


class AsyncCachedFetchWithConverter(AsyncCachedFetch):
	converter: Callable[[Output], ConvertedOutput]

	def __init__(self, async_callable: Call, converter: Callable[[Output], ConvertedOutput]):
		self.converter = converter
		super().__init__(async_callable)

	async def get(self) -> ConvertedOutput:
		return await super().get()

	async def fetch(self) -> ConvertedOutput:
		return self.converter(await super().fetch())
