from collections.abc import Callable
from functools import wraps
from typing import Any, NoReturn

from .tcr_void import void


class MayNotReturn:
  """Denote a return value for a function that may or may not return."""


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

    def wrap(func: Callable, exception=exception, excepth=excepth, els=els, finaly=finaly):
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


if True:  # \/ # asert

  def asert(condition_func: Callable, errmsg: str | None = None, *args: Any, **kwargs: Any) -> Any | MayNotReturn:
    if not condition_func(*args, **kwargs):
      if errmsg:
        raise AssertionError(errmsg)
      raise AssertionError
