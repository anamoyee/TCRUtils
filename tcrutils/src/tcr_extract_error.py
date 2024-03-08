import contextlib
import traceback

from .tcr_compare import able
from .tcr_iterable import getattr_queue


def extract_error(e: BaseException, pattern='%s: %s', *, raw=False) -> tuple[str, str] | str:
  if able(issubclass, e, BaseException) and issubclass(e, BaseException):
    tup = (getattr_queue(e, '__name__', '__class__.__name__', default='!UnknownExceptionGroupClass'), '<class>')
    return tup if raw else pattern % tup

  if able(issubclass, e, Exception) and issubclass(e, Exception):
    tup = (getattr_queue(e, '__name__', '__class__.__name__', default='!UnknownExceptionClass'), '<class>')
    return tup if raw else pattern % tup

  if callable(e):
    e = e()

  one = getattr_queue(e, '__name__', '__class__.__name__', default='!UnknownException')
  two = str(e)
  return (one, two) if raw else pattern % (one, two)


def extract_traceback(e: BaseException) -> str:
  traceback_details = traceback.format_tb(e.__traceback__)
  return ''.join(traceback_details)
