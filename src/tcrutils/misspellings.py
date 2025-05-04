from collections.abc import Callable


def asert[**P](predicate: Callable[P, bool], errmsg: str | None = None, *args: P.args, **kwargs: P.kwargs) -> None:
	"""If predicate(*args, **kwargs) returns a falsey value, raise an assertion error. This is different from the `assert` statement, as this will never be optimized out with the `python -O` flag."""
	if not predicate(*args, **kwargs):
		if errmsg:
			raise AssertionError(errmsg)
		raise AssertionError
