"""### This code was not written by me, however it's licensed with the MIT License which allows for free copy and sublicensing of the licensed material.

This code was written by [James Murphy](https://github.com/jamesmurphy-mc) from [MCoding](https://github.com/mCodingLLC/) ([YouTube](https://www.youtube.com/@mCoding))

[Original Source Code](https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/077_metaclasses_in_python/overloading.py)

Copy of the original license (applies only to this file):

```txt
MIT License

Copyright (c) 2022 MCODING, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Small modifications were made to this code
"""

import inspect

from .tcr_error import NoMatchingOverloadError


def _type_hint_matches(obj, hint):
  # only works with concrete types, not things like Optional
  return hint is inspect.Parameter.empty or isinstance(obj, hint)


def _signature_matches(sig: inspect.Signature, bound_args: inspect.BoundArguments):
  # doesn't handle type hints on *args or **kwargs
  for name, arg in bound_args.arguments.items():
    param = sig.parameters[name]
    hint = param.annotation
    if not _type_hint_matches(arg, hint):
      return False
  return True


def overload(func):
  """Decorator used to mark function as overload. Used in conjunction with tcr.OverloadMeta."""
  func.__overload__ = True
  return func


class OverloadList(list):
  pass


class _Overload:
  def __set_name__(self, owner, name):
    self.owner = owner
    self.name = name

  def __init__(self, overload_list):
    if not isinstance(overload_list, OverloadList):
      raise TypeError('must use OverloadList')
    if not overload_list:
      raise ValueError('empty overload list')
    self.overload_list = overload_list
    self.signatures = [inspect.signature(f) for f in overload_list]

  def __repr__(self):
    return f'{self.__class__.__qualname__}({self.overload_list!r})'

  def __get__(self, instance, _owner=None):
    if instance is None:
      return self
    # don't use owner == type(instance)
    # we want self.owner, which is the class from which get is being called
    return BoundOverloadDispatcher(instance, self.owner, self.name, self.overload_list, self.signatures)

  def extend(self, other):
    if not isinstance(other, _Overload):
      raise TypeError
    self.overload_list.extend(other.overload_list)
    self.signatures.extend(other.signatures)


class BoundOverloadDispatcher:
  def __init__(self, instance, owner_cls, name, overload_list, signatures):
    self.instance = instance
    self.owner_cls = owner_cls
    self.name = name
    self.overload_list = overload_list
    self.signatures = signatures

  def best_match(self, *args, **kwargs):
    for f, sig in zip(self.overload_list, self.signatures):  # noqa: B905
      try:
        bound_args = sig.bind(self.instance, *args, **kwargs)
      except TypeError:
        pass  # missing/extra/unexpected args or kwargs
      else:
        bound_args.apply_defaults()
        # just for demonstration, use the first one that matches
        if _signature_matches(sig, bound_args):
          return f

    raise NoMatchingOverloadError()

  def __call__(self, *args, **kwargs):
    try:
      f = self.best_match(*args, **kwargs)
    except NoMatchingOverloadError:
      pass
    else:
      return f(self.instance, *args, **kwargs)

    # no matching overload in owner class, check next in line
    super_instance = super(self.owner_cls, self.instance)
    super_call = getattr(super_instance, self.name, _MISSING)
    if super_call is not _MISSING:
      return super_call(*args, **kwargs)
    else:
      raise NoMatchingOverloadError()


_MISSING = object()


class OverloadDict(dict):
  def __setitem__(self, key, value):
    assert isinstance(key, str), 'keys must be str'

    prior_val = self.get(key, _MISSING)
    overloaded = getattr(value, '__overload__', False)

    if prior_val is _MISSING:
      insert_val = OverloadList([value]) if overloaded else value
      super().__setitem__(key, insert_val)
    elif isinstance(prior_val, OverloadList):
      if not overloaded:
        raise ValueError(self._errmsg(key))
      prior_val.append(value)
    else:
      if overloaded:
        raise ValueError(self._errmsg(key))
      super().__setitem__(key, value)

  @staticmethod
  def _errmsg(key):
    return f'must mark all overloads with @overload: {key}'


class OverloadMeta(type):
  """Overload Metaclass. Used in conjunction with @tcr.overload decorator.

  ```py
  class A(metaclass=OverloadMeta):
      @overload
      def f(self, x: int):
          print('A.f int overload', self, x)

      @overload
      def f(self, x: str):
          print('A.f str overload', self, x)

      @overload
      def f(self, x, y):
          print('A.f two arg overload', self, x, y)


  class B(A):
      def normal_method(self):
          print('B.f normal method')

      @overload
      def f(self, x, y, z):
          print('B.f three arg overload', self, x, y, z)

      # works with inheritance too!


  class C(B):
      @overload
      def f(self, x, y, z, t):
          print('C.f four arg overload', self, x, y, z, t)
  """

  @classmethod
  def __prepare__(mcls, name, bases):  # noqa: N804
    return OverloadDict()

  def __new__(mcls, name, bases, namespace, **kwargs):  # noqa: N804
    overload_namespace = {key: _Overload(val) if isinstance(val, OverloadList) else val for key, val in namespace.items()}
    return super().__new__(mcls, name, bases, overload_namespace, **kwargs)


class Overload(metaclass=OverloadMeta):
  """Overload Class. Used in conjunction with @tcr.overload decorator.

  ```py
  class A(Overload):
      @overload
      def f(self, x: int):
          print('A.f int overload', self, x)

      @overload
      def f(self, x: str):
          print('A.f str overload', self, x)

      @overload
      def f(self, x, y):
          print('A.f two arg overload', self, x, y)


  class B(A):
      def normal_method(self):
          print('B.f normal method')

      @overload
      def f(self, x, y, z):
          print('B.f three arg overload', self, x, y, z)

      # works with inheritance too!


  class C(B):
      @overload
      def f(self, x, y, z, t):
          print('C.f four arg overload', self, x, y, z, t)
  """


__all__ = ['overload', 'Overload', 'OverloadMeta', 'NoMatchingOverloadError']
