import asyncio as aio
from collections.abc import Callable, Coroutine
from typing import Any

type RunSACAble = Callable | Coroutine


async def run_sac(func_or_coro: RunSACAble, *args, **kwargs) -> Any:
	"""Run any function, async function or coroutine and return the result."""
	if aio.iscoroutine(func_or_coro):
		if args or kwargs:
			raise ValueError("Invalid arguments when using with coro")
		return await func_or_coro

	if aio.iscoroutinefunction(func_or_coro):
		return await func_or_coro(*args, **kwargs)

	if callable(func_or_coro):
		return func_or_coro(*args, **kwargs)

	msg = "func_or_coro must be a callable or coroutine."
	raise TypeError(msg)
