from collections.abc import Callable
from typing import Any


def insist(
	func: Callable[[], Any],
	validator: Callable[[Any], bool] = bool,
	func2: Callable[[], Any] | None = None,
):
	"""### Keep invoking `func` until `validator(func())` returns Truey result, return it.

	# Use `functools.partial` for this!!!

	```py
	from functools import partial
	number = int(insist(
	  partial(input, "Input a number: "),
	  partial(tcr.able, int)
	))
	```

	`func2` is invoked on 2nd and every later iteration, unless not provided, in that case `func` is invoked at all times.

	Keep in mind that insist won't convert the, str that was returned by `input()` in the above example, only verify its compliance with validator.
	"""
	result = func()
	if validator(result):
		return result
	while True:
		result = (func2 or func)()
		if not validator(result):
			continue

		return result
