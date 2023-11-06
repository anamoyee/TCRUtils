import time
from collections.abc import Callable
from functools import partial, wraps

from .tcr_color import color as c
from .tcr_void import void

if True:  # \/ # @test

  def test(func: Callable) -> Callable:
    """A decorator for adding."""

    @wraps(func)
    def wrapper(*args, **kwargs):
      name = func.__name__
      print(
        f"""
  {c('White')}####{len(name)*"#"}####
  {""}### {c('Gold')}{    name     }{c('White')} ###
  {""}####{len(name)*"#"}####{c('reset')}
  """[1:-1]
      )
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
          'c_White': c('White') if color else '',
          'c_Gold': c('Gold') if color else '',
          'c_reset': c('reset') if color else '',
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
      pattern='%(c_White)s%(name)s%(c_Gold)s took %(c_White)s%(time)s%(c_Gold)s seconds to execute.%(c_reset)s',
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

if True:  # \/ # @autorun

  def autorun(func):
    func()
    return func


if True:  # \/ # @trei

  def trei(
    exception: BaseException = Exception,
    excepth: Callable = void,
    els: Callable = void,
    finaly: Callable = void,
  ) -> Callable:
    if not issubclass(exception, BaseException):
      msg = f'exception must be an instance of BaseException (got {type(exception)}, {exception})'
      raise TypeError(msg)

    def wrap(
      func: Callable, exception=exception, excepth=excepth, els=els, finaly=finaly
    ):
      @wraps(func)
      def wrapper(*args, **kwargs):
        try:
          res = func(*args, **kwargs)
        except exception as e:
          excepth(e, *args, **kwargs)
        else:
          els(res, *args, **kwargs)
        finally:
          finaly(*args, **kwargs)

      return wrapper

    return wrap
