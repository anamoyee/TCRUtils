import contextlib
from collections.abc import Generator, Hashable, Mapping
from typing import Any

from .compare import isdunder


def _check_strict(master: Mapping, slave: Mapping, *, recursive: bool) -> bool:
	for k, v in master.items():
		if k not in slave:
			return [k]
		if recursive and isinstance(v, Mapping) and isinstance(slave[k], Mapping):
			if (a := _check_strict(v, slave[k], recursive=recursive)) is not True:
				return [k, *a]
	return True


def dict_zip(dict1: Mapping, *dicts: Mapping) -> Generator[tuple[Hashable, Any], None, None]:
	"""Zips dictionaries simillar to `zip()`, returns a generator which yields a tuple of (key, (value1, value2, value3)) for each key. This function does not support analogy of `zip()` non-strict mode, strict=True is implied (Each key must be in every single passed in dict)."""

	dicks = [dict1, *dicts]

	kys = dicks[0].keys()
	if any(kys != dick.keys() for dick in dicks):
		msg = "Mismatched keys"
		raise ValueError(msg)

	for k, v in dicks[0].items():
		yield (k, (v, *(dick[k] for dick in dicks[1:])))


def merge_dicts(master: Mapping = None, slave: Mapping = None, *dicts: Mapping, recursive=True, strict=False) -> dict:
	"""Merge dictionaries, made to prioritize the `master` dictionary and if key is not found there, then it takes from the `slave` dictionary.

	Optionally if `recursive=True`, then if the same key is a dict in both master and slave, merge dicts operation is performed on both of them.\\
	Optionally if `strict=True` it raises `ValueError` if there exists a key that is in master dictionary but not in slave dictionary.\\
	If there are more than 2 arguments passed in the list is reduced from back to front until two elements are left by the process of merge_dicts(master=list[-2], slave=list[-1])
	"""
	merged = {}

	if master is None:
		master = {}
	if slave is None:
		slave = {}

	dicts = [master, slave, *dicts]

	while len(dicts) > 2:
		slave_ = dicts.pop()
		master_ = dicts[-1]
		dicts[-1] = merge_dicts(master_, slave_, recursive=recursive, strict=strict)

	master, slave = dicts

	if strict:
		a = _check_strict(master, slave, recursive=recursive)
		if a is not True:
			msg = f"Strict check failed: there exists a key ({'.'.join(repr(x) for x in a)}) that is in master dictionary but not in slave dictionary"
			raise ValueError(msg)

	for key in master:
		if key in slave:
			if isinstance(master[key], dict) and isinstance(slave[key], dict) and recursive:
				merged[key] = merge_dicts(master[key], slave[key], recursive=True)
			else:
				merged[key] = master[key]
		else:
			merged[key] = master[key]

	for key in slave:
		if key not in merged:
			merged[key] = slave[key]

	return merged


def clean_dunder_dict(
	__dict__: dict[str, Any],
	strategy: int = 1,
) -> dict:
	"""Filter the __dict__ passed in (or any other str-keyed dict for that matter).

	Strategy types:
	- 0: Remove only __dunder__ keys
	- 1: 0™ and also remove __double_underscore_prefixed keys (default)
	- 2: 1™ and also remove _single_underscore_prefixed keys
	"""

	if strategy == 0:
		return {x: y for x, y in __dict__.items() if not (x.startswith("__") and x.endswith("__"))}

	if strategy == 1:
		return {x: y for x, y in __dict__.items() if not x.startswith("__")}

	if strategy == 2:
		return {x: y for x, y in __dict__.items() if not x.startswith("_")}

	if strategy == -2:
		raise ValueError("Invalid strategy, choose 0, 1 or 2 (not literally `0-2` you fucking idiot)")

	raise ValueError("Invalid strategy, choose 0-2")


class DotDict(dict):
	"""### dot.notation access to dictionary attributes.

	This will ignore any dunder attributes, and will not try to look them up in the underlying dict.

	```py
	>>> d = {"a": 1, "b": 2}
	>>> dd = DotDict(d) # or DotDict({"a": ...})
	>>> dd.a
	1
	>>> dd.b
	2
	```

	This will convert any Mapping that is not already a DotDict into a DotDict on access.

	Raises:
	    - KeyError (tried to convert the dot-access to item-access but failed to find item)
	    - AttributeError (the dot-accessed attribute was dunder, did not try to convert to item-access and said attribute was not found)
	    - Other standard dict errors if any.
	"""

	def __getattr__(self, attr):
		if isdunder(attr):
			return object.__getattribute__(self, attr)

		a = super().__getitem__(attr)

		if not isinstance(a, DotDict) and isinstance(a, Mapping):
			return DotDict(a)

		return a

	def __setattr__(self, attr, value):
		if isdunder(attr):
			return setattr(self, attr, value)

		super().__setitem__(attr, value)

	def __delattr__(self, attr):
		if isdunder(attr):
			return delattr(self, attr)

		super().__delitem__(attr)
