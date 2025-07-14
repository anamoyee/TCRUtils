import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable, Generator
from typing import Any, Self

from .print import TcrFmt_KwargsDataclass
from .result import Result


def _filter_out_nones_in_place(results: list[Any | None]) -> None:
	results[:] = [r for r in results if r is not None]


def _filter_out_none_results_in_place(results: list[Result[Any | None, Any]]) -> None:
	results[:] = [r for r in results if (r.is_err or r.unwrap() is not None)]


# py313: class BaseEvent[R: Any = None](TcrFmt_KwargsDataclass):
class BaseEvent[R: Any](TcrFmt_KwargsDataclass):
	"""Represents a base event, kind of like BaseException represents base exception. Generic on the return value."""

	_subscribers = defaultdict(set)

	@classmethod
	def subscribe(cls, func: Callable[[Self], Awaitable[R]]):
		"""Subscribe to an event by passing a function shaped as: `async (Event) -> Event<R>::R`."""
		if not asyncio.iscoroutinefunction(func):
			raise TypeError("Subscriber must be an async function")
		cls._subscribers[cls].add(func)
		return func

	def _iter_subscriber_calls(self) -> Generator[Callable[[Self], Awaitable[R]]]:
		for cls in type(self).mro():
			if not issubclass(cls, BaseEvent):
				continue

			yield from self._subscribers.get(cls, set())

	async def emit_results(self, *, filter_out_nones: bool = False) -> tuple[Result[R, Exception], ...]:
		"""Emit the event instance, calling & awaiting all relevant subscribers. Returns a tuple of all subscriber return values (if subscriber raises, appropriate Result value is used in the given position)."""
		results = []
		for func in self._iter_subscriber_calls():
			try:
				current_returned = await func(self)
			except Exception as e:
				results.append(Result.new_err(e))
			else:
				results.append(Result.new_ok(current_returned))

		if filter_out_nones:
			_filter_out_none_results_in_place(results)

		return tuple(results)

	async def emit_excgroup(self, *, filter_out_nones: bool = False) -> tuple[R, ...]:
		"""Emit the event instance, calling & awaiting all relevant subscribers. Returns a tuple of all subscriber return values (if subscriber raises, an exception group is raised, emitting continues, and at the end the accumulated exceptions in the exception group are raised)."""
		results = []
		exceptions = []

		for func in self._iter_subscriber_calls():
			try:
				results.append(await func(self))
			except Exception as e:
				exceptions.append(e)

		if exceptions:
			raise ExceptionGroup(f"{self.__class__.__name__}: During event emission at least 1 subscriber raised an exception", exceptions)

		if filter_out_nones:
			_filter_out_nones_in_place(results)

		return tuple(results)

	async def emit_failfast(self, *, filter_out_nones: bool = False) -> tuple[R, ...]:
		"""Emit the event instance, calling & awaiting all relevant subscribers. Returns a tuple of all subscriber return values (if subscriber raises, dont catch the error, the emission ends immediately)."""
		results = []

		for func in self._iter_subscriber_calls():
			results.append(await func(self))

		if filter_out_nones:
			_filter_out_nones_in_place(results)

		return tuple(results)


if __name__ == "__main__":

	async def __main():  # Basic inline testing
		import pydantic as pd

		from .console import c

		class BM(pd.BaseModel):
			model_config = pd.ConfigDict(
				arbitrary_types_allowed=True,
				validate_assignment=True,
			)

		class UserEvent(BaseEvent[str]):
			def __init__(self, username: str):
				self.username = username

		class UserLoginEvent(UserEvent):
			def __init__(self, username: str):
				super().__init__(username)

		class PydanticEvent(BM, BaseEvent[str]):
			userid: int

		####################

		@UserLoginEvent.subscribe
		async def on_user_login(event: UserLoginEvent):
			print(f"User {event.username} logged in.")
			return "Login Handled"

		@UserEvent.subscribe
		async def on_any_user_event(event: UserEvent):
			print(f"User event detected: {event!r}")
			return "User Event Processed"

		######

		class BadEvent(BaseEvent): ...

		@BadEvent.subscribe
		async def bad_callback(event: BadEvent):
			raise ValueError("whyvent")

		@BadEvent.subscribe
		async def ok_callback(event: BadEvent):
			return "ok"

		for _ in range(10):

			@BadEvent.subscribe
			async def bad_callback2(event: BadEvent):
				raise RuntimeError("evąt")

		#######

		@PydanticEvent.subscribe
		async def on_pydantic_event(event: PydanticEvent):
			print(f"Pydantic event detected: {event.userid!r}")
			return "Pydantic Event Processed"

		if True:  # happy path
			event = UserLoginEvent("Alice")
			results = await event.emit_excgroup()
			c("Subscribers returned:", results)

			c.hr()

			event = UserLoginEvent("Alice")
			results = await event.emit_results()
			c("Subscribers returned:", results)

			c.hr()

			event = UserLoginEvent("Alice")
			results = await event.emit_failfast()
			c("Subscribers returned:", results)

			c.hr()

		if True:  # Pydantic happy path
			event = PydanticEvent(userid=42)
			results = await event.emit_excgroup()
			c("Subscribers returned:", results)

		if True:  # Printing
			c(UserLoginEvent("alice"))
			c(PydanticEvent(userid=42))
			c(UserLoginEvent)
			c(PydanticEvent)

		if False:  # bad path
			event = BadEvent()
			results = await event.emit_results()
			c("Bad Subscribers returned:", results)

			c.hr()

			event = BadEvent()
			results = await event.emit_excgroup()
			c("Bad Subscribers returned:", results)

			c.hr()

	asyncio.run(__main())
