from typing import Self


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


class SingletonForced:
  """Force single instance at all times by raising an error if one was already created.

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
