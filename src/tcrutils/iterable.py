import re as regex
from collections.abc import Callable, Iterable, Iterator, MutableSequence
from random import shuffle
from typing import Any, Literal, TypeVar

from .compare import able
from .regex import RegexPreset

T = TypeVar("T")
Ts = TypeVar("Ts")


def batched(
	it: Iterable[T],
	n: int,
	*,
	back_to_front: bool = False,
) -> list[Iterable[T]]:
	"""### Poor man's `itertools.batched()` (on Py3.11).

	itertools.batched exists but I left it here because:
	- I still need to support py3.11
	- I don't think itertools.batched() has an option to easily back_to_front the results.

	Return a list of splits of the original `it` Iterable that was passed in, split every `n` items. Last group may be smaller than `n` items if the source was exhausted
	`back_to_front`: makes the items pile up in the back and now the first item is the one to have less than n items if there's not enough to pack it with. For example:
	- `batched("1234567890", n=3)                    ` returns `["123", "456", "789", "0"]`
	- `batched("1234567890", n=3, back_to_front=True)` returns `["1", "234", "567", "890"]`
	"""
	if back_to_front:
		return [x[::-1] for x in batched(it[::-1], n=n, back_to_front=False)[::-1]]
	return [it[i : i + n] for i in range(0, len(it), n)]


def cut_at(
	it: str | Iterable,
	n: int,
	end: str | Iterable = "...",
	*,
	filter_links: Literal[False] | str | Callable = False,
	shrink_links_visually_if_fits: bool = False,
) -> str:
	"""### Return a cut off part of the provided `it` iterable.

	with the `end` added at the end such that the return value is exactly `n` in length.\\
	Mainly strings but also supports other iterables\\
	Set `end` to `''`/`[]` to disable it.\\

	Use `filter_links` to shorten links to this string, only applicable if the iterable provided is a string and if the iterable exceeded `n`, else nothing will be affected
	- `$1` - Entire link
	- `$2` - http/https (will keep the 's' if present, that's its point)
	- `$3` - any `subdomains.` (if present), `.domains.` or `.tld`s
	- `$4` - `.domain` (second to last (possibly after . and) before the last .)
	- `$5` - `.tld` (in between the last . and / or end of match)
	- `$6` - part of the link after `/` (not including it, may be '')

	https://regex101.com/r/46LZtS/1

	`shrink_links_visually_if_fits` replaces links with their markdown counterparts where the visible text is http(s):/subdomain.domain.tld/ (no further part of the links is visible, but the entire link is contained)
	"""
	if len(it) <= n:
		if shrink_links_visually_if_fits and len(a := regex.sub(RegexPreset.URL, r"[\2:/\3/](<\1>)", it)) <= n:  # :/ instead of :// because discord bruh
			return a
		return it
	if filter_links is not False and isinstance(it, str):
		if not isinstance(filter_links, str | Callable):
			msg = f"Set filter_links to a str of the replacement value for links or Callable, not {filter_links!r}"
			raise ValueError(msg)
		it = regex.sub(RegexPreset.URL, filter_links, it)
		if len(it) <= n:
			return it
	if n > len(end):
		return it[: (n - len(end))] + end
	if n > 0:
		return end[:n]
	return ""


def bogo_sort(arr: list[T]) -> list[T]:
	if 0 <= len(arr) <= 1:
		return arr
	while True:
		shuffle(arr)
		for i in range(len(arr) - 1):
			if arr[i] > arr[i + 1]:
				break
		else:
			return arr


def stalin_sort(arr: Iterable[T]) -> list[T]:
	if len(arr) <= 1:
		return arr

	sorted_arr = [arr[0]]

	for i in range(1, len(arr)):
		if arr[i] >= sorted_arr[-1]:
			sorted_arr.append(arr[i])

	return sorted_arr


def shuffled(arr: MutableSequence[T]) -> MutableSequence[T]:
	shuffle(arr)
	return arr


def limited_iterable(it: Iterable[T] | Iterator[T], limit: int) -> tuple[list[T], int]:
	"""## Return tuple[list, int] of (limited_iterable, overflow_from_limit).

	### This is different from it[:limit] because it works with iterators

	Examples:
	```py
	>>> limited_iterable([10, 20, 30], 10)
	([10, 20, 30], 0) # Nothing is cut off
	>>> limited_iterable([10, 20, 30], 3)
	([10, 20, 30], 0)
	>>> limited_iterable([10, 20, 30], 2)
	([10, 20], 1)
	>>> limited_iterable([10, 20, 30], 1)
	([10], 2)
	>>> limited_iterable([10, 20, 30], 0)
	([], 3)
	>>> limited_iterable([10, 20, 30], -1)
	([], 4) # Overflow counter counts the negative limit even though it makes no sense, for predictability reasons
	```
	---

	### When there's no len method on the passed in iterable (eg. generator) and the iterable takes longer than the limit the overflow returned is -1**

	```py
	>>> limited_iterable(range(10), 7)
	([0, 1, 2, 3, 4, 5, 6], 3) # range by itself has len support even though it's a generator due to comparing boundaries
	>>> limited_iterable(iter(range(10)), 7)
	([0, 1, 2, 3, 4, 5, 6], -1) # when wrapped into an iter() the length can't be determined within the limit
	>>> limited_iterable(iter(range(5)), 7)
	([0, 1, 2, 3, 4], 0) # 0 was returned even though it's a non-len object because the iterator was exhausted and the end of it being within limit could be determined.
	```
	"""
	if limit <= 0:
		return ([], len(it) - limit if able(len, it) else -1)
	list_ = []
	breaknext = False
	for i, item in enumerate(it):
		if breaknext:
			return breaknext
		list_.append(item)
		if i + 2 > limit:
			overflow = len(it) - limit if able(len, it) else -1
			breaknext = (list_, overflow)
	return list_, 0


def hasmanyattrs(obj, attr: str, *attrs: str) -> bool:
	attrs = (attr, *attrs)

	for attr in attrs:
		if not hasattr(obj, attr):
			return False

		obj = getattr(obj, attr)

	return True


def getmanyattrs(obj, attr: str, *attrs: str) -> Any:
	attrs = (attr, *attrs)

	for attr in attrs:
		obj = getattr(obj, attr)

	return obj


RaiseError = object()


def getattr_queue(
	obj: object,
	/,
	*queue: str,
	return_as_str: bool = False,
	default: Any = RaiseError,
):
	"""## Try to access `obj`'s attrs in order.

	```py
	queue = ('__qualname__', '__name__')

	getattr(obj, '__qualname__') # return this if hasattr(obj, '__qualname__') else go to the next line
	getattr(obj, '__name__')     # return this if hasattr(obj, '__name__') else go to the next line
	if default is not RaiseError # RaiseError is the default value for default (if nothing is passed in)
	  return default
	raise KeyError("Unable to find any attrs from queue in obj.") # Nothing could be found, error raised.
	```

	In other words: try to get name #1, if not found, get name #2, if not found get #3, etc. etc. until the queue is exhausted.
	"""
	if not queue:
		raise ValueError("queue cannot be empty.")
	for name in queue:
		if hasmanyattrs(obj, *name.split(".")):
			if return_as_str:
				return name
			else:
				return getmanyattrs(obj, *name.split("."))
	if default is not RaiseError:
		return default
	raise KeyError("Unable to find any attrs from queue in obj.")


def Or(arg: T, *args: Ts, none: Any = None) -> T | Ts:
	"""### Returns the first element of the tuple (arg, *args) that does not equal the supplied (`none`) variable, by default None.

	This is different from or chaining because this does not check for truthy values but rather non-none values.\\
	Keep in mind, the passed in none may be unrelateed to built-in None however that is its default.
	"""
	args = (arg, *args)

	for a in args:
		if a != none:
			return a

	return args[-1]


def slice_between(lst: Iterable, /, left=None, right=None, *, flip_on_left_right_mismatch: bool = True) -> Iterable:
	if lst:
		if left is None:
			left = lst[0]
		if right is None:
			right = lst[-1]
	else:
		raise KeyError(f"Unable to infer the list boundaries: the list is empty.")

	if left not in lst:
		raise KeyError(f"Left boundary {left!r} not found in the list.")
	if right not in lst:
		raise KeyError(f"Right boundary {right!r} not found in the list.")

	left_index = lst.index(left)
	right_index = lst.index(right)
	if left_index > right_index:
		if flip_on_left_right_mismatch:
			left_index, right_index = right_index, left_index
		else:
			raise ValueError("Left boundary cannot be to the right of the right boundary and flip_on_left_right_mismatch=False.")

	return lst[left_index : right_index + 1]
