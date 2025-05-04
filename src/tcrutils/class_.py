import time
from collections import OrderedDict
from typing import Any, Self


class Singleton:
	"""Keep single instance at all times.

	## Make sure to put the `tcr.Singleton` inheretance before all others!
	### ❌ `class A(B, tcr.Singleton)`
	### ✅ `class A(tcr.Singleton, B)`

	```py
	class SingleTuple(tcr.Singleton, tuple):
	    ...

	  tup = SingleTuple(('tup1',))
	  tup2 = SingleTuple(('tup2',)) # Those arguments are effectively ignored

	  console(tup)  # -> ('tup1',)
	  console(tup2) # -> ('tup1',)
	```
	"""

	__singleton_instance__ = None

	def __new__(cls, *args, **kwargs) -> Self:
		if cls.__singleton_instance__ is None:
			cls.__singleton_instance__ = super().__new__(cls, *args, **kwargs)
		return cls.__singleton_instance__


class NoInit:
	def __init__(self, *args, **kwargs) -> None:
		msg = "You cannot instiantiate this class"

		if hasattribute(self, "__noinit_msg"):
			msg = str(getattr(self, "__noinit_msg"))

		raise RuntimeError(msg)


def partial_class(_f=None, /, *, add_as_kwargs_to_init: bool = True) -> type:
	"""### Simillarly to functools.partial allows subclasses of decorated class to hold a meta-like state to be later used in e.g. root's init or anywhere else.

	```py
	@tcr.partial_class
	class Button:
	  def __init__(self, label: str):
	    self.label = label

	  def __repr__(self):
	    return f'Button(label={self.label!r})'

	class YesButton(Button, label='Yes'): ...
	class NoButton(Button, label='No'): ...

	y = YesButton()
	c(repr(y)) # -> Button(label='Yes')
	n = NoButton()
	c(repr(n)) # -> Button(label='No')
	n2 = NoButton(label='Nuh uh') # Overridden
	c(repr(n2)) # -> Button(label='Nuh uh')
	```

	Args:
	  add_as_kwargs_to_init: bool = True. If True, the state  will be passed as keyword arguments into `__init__`.
	"""

	def decorator(cls: type) -> type:
		def new_init_subclass(new_cls, **kwargs) -> None:
			new_cls._partial_state = kwargs

			if not add_as_kwargs_to_init:
				return

			original_init = new_cls.__init__

			def new_init(self, *args, **init_kwargs):
				merged_kwargs = {**self._partial_state, **init_kwargs}  # Merge both states such that caller can override it, like functools.partial
				original_init(self, *args, **merged_kwargs)

			new_cls.__init__ = new_init

		cls.__init_subclass__ = classmethod(new_init_subclass)
		return cls

	if _f is not None:
		return decorator(_f)
	return decorator


def hasattribute(obj: object, name: str) -> bool:
	try:
		object.__getattribute__(obj, name)
	except AttributeError:
		return False
	else:
		return True


class DefaultsGetSetItem(dict):
	def __getitem__(self, __key: Any, /) -> Any:
		try:
			return super().__getitem__(__key)
		except KeyError:
			if hasattribute(self, "defaults") and __key in (defaults := object.__getattribute__(self, "defaults")):
				val = defaults[__key]()
				self[__key] = val
				return val
			else:
				raise


class DefaultsGetItem(dict):
	def __getitem__(self, __key: Any, /) -> Any:
		try:
			return super().__getitem__(__key)
		except KeyError:
			if hasattribute(self, "defaults") and __key in (defaults := object.__getattribute__(self, "defaults")):
				return defaults[__key]()
			else:
				raise


class DefaultsGetSetAttr:
	def __getattr__(self, __name: str, /) -> Any:
		try:
			return getattr(super(), __name)
		except AttributeError as e:
			if hasattribute(self, "defaults") and __name in (defaults := object.__getattribute__(self, "defaults")):
				val = defaults[__name]()
				self.__setattr__(__name, val)
				return val
			else:
				raise AttributeError(f"{self.__class__.__name__!r} object has no attribute nor default value for {__name!r}") from e


class DefaultsGetAttr:
	def __getattr__(self, __name: str, /) -> Any:
		try:
			return getattr(super(), __name)
		except AttributeError as e:
			if hasattribute(self, "defaults") and __name in (defaults := object.__getattribute__(self, "defaults")):
				return defaults[__name]()
			else:
				raise AttributeError(f"{self.__class__.__name__!r} object has no attribute nor default value for {__name!r}") from e


class CachedInstancesMeta(type):
	"""Metaclass for caching instances based on init parameters with customizable max time and max instances."""

	def __new__(
		mcls,  # noqa: N804
		name,
		bases,
		dct,
		max_instances: int = 50,
		max_time: int = 30 * 60,
		restore_method: str | None = None,
	):
		cls = super().__new__(mcls, name, bases, dct)
		cls._cache = OrderedDict()
		cls._max_instances = max_instances
		cls._max_time = max_time
		cls._restore_method = restore_method
		return cls

	def __call__(cls, *args, **kwargs):
		key = (args, tuple(sorted(kwargs.items())))

		cls._remove_old_instances()

		if key in cls._cache:
			instance, _ = cls._cache.pop(key)
			cls._cache[key] = (instance, time.time())

			if instance._restore_method is not None:
				getattr(instance, instance._restore_method)()
			return instance

		instance = super().__call__(*args, **kwargs)

		cls._cache[key] = (instance, time.time())

		cls._enforce_max_cache_size()

		return instance

	def _remove_old_instances(cls):
		current_time = time.time()
		keys_to_remove = []
		for key, (_, timestamp) in cls._cache.items():
			if current_time - timestamp > cls._max_time:
				keys_to_remove.append(key)
		for key in keys_to_remove:
			del cls._cache[key]

	def _enforce_max_cache_size(cls):
		while len(cls._cache) > cls._max_instances:
			cls._cache.popitem(last=False)


def new_cell():
	return (lambda: a).__closure__[0].__class__()  # type: ignore <-- hehe :3
	a = 1
