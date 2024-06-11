import inspect
import time
from asyncio import iscoroutinefunction
from collections.abc import Callable
from functools import partial, wraps

from colored import Back, Fore, Style

from .tcr_print import print_block

if True:  # \/ # @test

  def test(func: Callable) -> Callable:
    """A decorator for adding test label."""

    @wraps(func)
    def wrapper(*args, **kwargs):
      name = func.__name__
      name = name.removeprefix('test_')
      name = name.replace('_', ' ')
      name = name.title()
      print_block(name)
      return func(*args, **kwargs)

    return wrapper


if True:  # \/ # @timeit // timeit.start() and .stop()

  class Timeit:
    t: float | None
    tname: str

    def __init__(self) -> None:
      self.t = {}

    def _print_time(self, printhook, pattern, name, elapsed_time, color):
      printhook(
        pattern
        % {
          'name': name,
          'time': f'{elapsed_time:.4f}',
          'c_White': (Fore.white + Style.bold) if color else '',
          'c_Gold': (Fore.yellow + Style.bold) if color else '',
          'c_reset': Style.reset if color else '',
        }
      )

    def start(self, name='test'):
      self.t[name] = time.perf_counter()

    def stop(
      self,
      name='test',
      *,
      printhook=print,
      color=True,
      pattern='%(c_White)s%(name)s%(c_Gold)s took %(c_White)s%(time)s%(c_Gold)s seconds to execute.%(c_reset)s',
    ):
      if self.t.get(name) is None:
        msg = 'You cannot stop the timer if it was not started'
        raise RuntimeError(msg)
      diff = time.perf_counter() - self.t[name]
      self._print_time(printhook, pattern, name, diff, color)

    def __call__(
      self,
      func=None,
      *,
      printhook=None,
      color=True,
      pattern='\n%(c_White)s%(name)s%(c_Gold)s took %(c_White)s%(time)s%(c_Gold)s seconds to execute.%(c_reset)s\n',
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

if True:  # \/ # @autorun, @instance

  def autorun(func):
    func()
    return func

  def instance(func):
    return func()


if True:  # \/ # @convert.stringify

  class Convert:
    def stringify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return str(func(*args, **kwargs))

      return wrapper

    def intify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return int(func(*args, **kwargs))

      return wrapper

    def floatify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return float(func(*args, **kwargs))

      return wrapper

    def boolify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return bool(func(*args, **kwargs))

      return wrapper

    def listify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))

      return wrapper

    def setify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return set(func(*args, **kwargs))

      return wrapper

    def dictify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return dict(func(*args, **kwargs))

      return wrapper

    def tuplify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return tuple(func(*args, **kwargs))

      return wrapper

    def complexify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return complex(func(*args, **kwargs))

      return wrapper

    def reprify(self, func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        return repr(func(*args, **kwargs))

      return wrapper

    def anyify(self, converter: Callable):
      def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
          return converter(func(*args, **kwargs))

        return wrapper

      return decorator

  convert = Convert()

  def aconvert(converter: Callable, await_converter: bool = False):
    def decorator(afunc):
      @wraps(afunc)
      async def wrapper(*args, **kwargs):
        if await_converter:
          return await converter(await afunc(*args, **kwargs))
        else:
          return converter(await afunc(*args, **kwargs))

      return wrapper

    return decorator


if True:  # \/ # @printer

  def printer(*, printhook: Callable[[str], None] = print, passthrough: bool = True):
    def decorator(func: Callable):
      @wraps(func)
      def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        printhook(result)
        if passthrough:
          return result

      return wrapper

    return decorator


if True:  # \/ # @copy_kwargs

  def copy_kwargs(func):
    """Pack all of that func's kwargs into __kwargs and pass the kwarguments normally along with __kwargs kwarg which contains all the kwargs in a dict.

    This will error if func receives a literal "__kwargs" kwarg.
    ```py
    >>> a(__kwargs=kwargs, **{"__kwargs": "some_value"})
    ```
    ```txt
    TypeError: __main__.a() got multiple values for keyword argument '__kwargs'
    ```
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
      return func(*args, __kwargs=kwargs, **kwargs)

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
