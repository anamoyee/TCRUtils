import os
import sys
import time
from collections.abc import Awaitable, Callable
from functools import partial, wraps
from typing import overload

from colored import Back, Fore, Style

from .print import print_block

if True:  # \/ # @test

	def test(func: Callable):
		"""Print a "test label" with this function's name, in title case before it runs, so it is clear where one test starts (and other ends, if any)."""

		@wraps(func)
		def wrapper(*args, **kwargs):
			name = func.__name__
			name = name.removeprefix("test_")
			name = name.replace("_", " ")
			name = name.title()
			print_block(name)
			return func(*args, **kwargs)

		return wrapper


if True:  # \/ # @timeit // timeit.start() and .stop()

	class _Mock_dev_null:
		def write(self, s):
			return len(s)

		def flush(self):
			pass

		def read(self):
			return ""

		def close(self):
			pass

	class Timeit:
		t: dict[str, float | None]
		tname: str

		def __init__(self) -> None:
			self.t = {}

		def _print_time(self, printhook, pattern, name, elapsed_time, color):
			printhook(
				pattern
				% {
					"name": name,
					"time": f"{elapsed_time:.4f}",
					"c_White": (Fore.white + Style.bold) if color else "",
					"c_Gold": (Fore.yellow + Style.bold) if color else "",
					"c_reset": Style.reset if color else "",
				}
			)

		def start(self, name="test"):
			self.t[name] = time.perf_counter()

		def stop(
			self,
			name="test",
			*,
			printhook=print,
			color=True,
			pattern="%(c_White)s%(name)s%(c_Gold)s took %(c_White)s%(time)s%(c_Gold)s seconds to execute%(c_reset)s",
		):
			if self.t.get(name) is None:
				msg = "You cannot stop the timer if it was not started"
				raise RuntimeError(msg)
			diff = time.perf_counter() - self.t[name]
			self._print_time(printhook, pattern, name, diff, color)

		def __call__(
			self,
			func=None,
			*,
			printhook=None,
			color=True,
			pattern="%(c_White)s%(name)s%(c_Gold)s took %(c_White)s%(time)s%(c_Gold)s seconds to execute.%(c_reset)s",
		):
			if func is None:
				return partial(timeit, printhook=printhook, pattern=pattern, color=color)
			if printhook is None:
				printhook = print

			@wraps(func)
			def wrapper(*args, **kwargs):
				start_time = time.perf_counter()
				result = func(*args, **kwargs)
				end_time = time.perf_counter()
				elapsed_time = end_time - start_time
				self._print_time(printhook, pattern, func.__name__, elapsed_time, color)
				return result

			return wrapper

	timeit = Timeit()

	class TimeitPartial[**P]:
		name = ""
		currently_elapsed: float
		t: float | None
		partials: int

		def __init__(self, name: str = "", *, perf_counter=time.perf_counter):
			self.name = name
			self.perf_counter = perf_counter
			self.reset()

		def reset(self):
			self.currently_elapsed = 0.0
			self.t = None
			self.partials = 0

		def start(self):
			tmp = self.perf_counter()  # Maximize accuracy

			if self.t is not None:
				raise RuntimeError(f"Cannot start an already started {self.__class__.__name__}")

			self.t = tmp

		def stop(self):
			end = self.perf_counter()  # Maximize accuracy

			if self.t is None:
				raise RuntimeError(f"Cannot stop a stopped (or never-started) {self.__class__.__name__}.")

			start = self.t
			self.t = None

			self.currently_elapsed += end - start
			self.partials += 1

		@overload
		def finish_and_print(self, **kwargs: P.kwargs): ...

		def finish_and_print(
			self,
			*,
			syntax_highlighting: bool = True,
			time_float_format_str: str = ".3f",
			printhook=print,
			reset: bool = True,
		) -> str:
			c_white = Fore.white + Style.bold if syntax_highlighting else ""
			c_gold = Fore.yellow + Style.bold if syntax_highlighting else ""
			c_reset = Style.reset if syntax_highlighting else ""

			msg = f"{c_reset}{c_white}{self.name or f'{c_gold}test'}{' ' if self.name != '' else ''}{c_gold}took {c_white}{self.currently_elapsed:{time_float_format_str}}{c_gold}s"

			if self.partials != 1:
				msg += f" with {c_white}{self.partials} {c_gold}partials"

			msg += c_reset

			printhook(msg)

			if reset:
				self.reset()

			return msg

		def decorator(self, **finish_and_print_kwargs):
			def decorator_inner(f):
				if self.name == "":
					self.name = f.__name__

				@wraps(f)
				def wrapper(*args, **kwargs):
					retv = f(*args, __timeit=self, **kwargs)
					tmp_currently_elapsed = self.currently_elapsed
					self.finish_and_print(**finish_and_print_kwargs)
					return (tmp_currently_elapsed, retv)

				return wrapper

			return decorator_inner

	def repeat[**P, R](n: int, *, no_stdout_after_first: bool = False):
		def decorator(f: Callable[P, R]):
			@wraps(f)
			def wrapper(*args: P.args, **kwargs: P.kwargs) -> list[tuple[float, R]]:
				values = []
				for i in range(n):
					if add_back_stdout := (no_stdout_after_first and i > 0):
						orig_sys_stdout = sys.stdout
						sys.stdout = _Mock_dev_null()
					values.append(f(*args, **kwargs))
					if add_back_stdout:
						sys.stdout.close()
						sys.stdout = orig_sys_stdout
				return values

			return wrapper

		return decorator


if True:  # \/ # @copy_kwargs

	def copy_kwargs(func):
		"""Pack all of that func's kwargs into __kwargs and pass the kwarguments normally along with __kwargs kwarg which contains all the kwargs in a dict.

		This will error if func receives a literal "__kwargs" kwarg.
		```
		>>> a(__kwargs=kwargs, **{"__kwargs": "some_value"})
		```
		```
		TypeError: __main__.a() got multiple values for keyword argument '__kwargs'
		```
		"""

		@wraps(func)
		def wrapper(*args, **kwargs):
			return func(*args, __kwargs=kwargs, **kwargs)

		return wrapper

	def copy_kwargs_sunder(func):
		"""Pack all of that func's kwargs into _kwargs and pass the kwarguments normally along with _kwargs kwarg which contains all the kwargs in a dict.

		This will error if func receives a literal "_kwargs" kwarg.
		```py
		>>> a(_kwargs=kwargs, **{"_kwargs": "some_value"})
		```
		```txt
		TypeError: __main__.a() got multiple values for keyword argument '_kwargs'
		```
		"""

		@wraps(func)
		def wrapper(*args, **kwargs):
			return func(*args, _kwargs=kwargs, **kwargs)

		return wrapper


if True:  # \/ # @skip_first_call

	def skip_first_call(func):
		func._first_call = True

		def wrapper(*args, **kwargs):
			if func._first_call:
				func._first_call = False
				return None
			else:
				return func(*args, **kwargs)

		return wrapper

	def skip_first_call_async(func):
		func._first_call = True

		async def wrapper(*args, **kwargs):
			if func._first_call:
				func._first_call = False
				return None
			else:
				return await func(*args, **kwargs)

		return wrapper


if True:  # \/ # @with_overrides

	def with_overrides(*overrides: str):
		"""For each of the passed in keyword argument names: if one was passed in by the user, use that one, else use `self.{name}`."""

		def decorator(func: Callable):
			def wrapper(self, *args, **kwargs):
				kws = kwargs.copy()
				for o in overrides:
					if o not in kwargs:
						kws[o] = getattr(self, o)

				return func(self, *args, **kws)

			return wrapper

		return decorator


if True:  # @autorun, @instance
	from collections.abc import Callable

	def autorun[**P, R, F: Callable[P, R]](f: F) -> F:
		f()
		return f

	def instance[R](f: Callable[[], R]) -> R:
		return f()

	if 1 - 1:
		# fmt: off
		if True: # @instance
			@instance
			class __A: ...

			reveal_type(__A.__class__)  # Should be `type[__A]`     #
			reveal_type(__A)            # Should be `__A`           #
			reveal_type(__A())          # Should be `Any` (unknown) #

		if True: # @autorun
			@autorun
			def __f(): ...

			reveal_type(__f)   # Should be `() -> None`, not `None` #
			reveal_type(__f()) # Should be `None`                   #
		# fmt: on
