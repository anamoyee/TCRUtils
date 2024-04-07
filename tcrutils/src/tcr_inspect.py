import inspect
import sys
from typing import TypeVar

T = TypeVar('T')


def get_lineno(*, default: T | None = None, backtrack_frames: int = 1) -> int | T:
  """Return the python file's line number at which this function was called as an int.

  Args:
    default: Any = None, will be returned if the function's calling place could not be determiend
    backtrack_frames: int = 1, how many frames to go back in the stack, if set to 1, will return the calling frame's line number, if set to 0 will return this module's internal line number (so dont) but may be useful when building a function that itself makes use of get_lineno() in which case you'd need to make it 2 so your function doesn't just return internal line number
  """
  frame = inspect.currentframe()
  for _ in range(backtrack_frames):
    if frame is None:
      return default
    frame = frame.f_back
  return frame.f_lineno if frame else default


def get_file_colon_lineno(default: T | None = None, backtrack_frames: int = 1, additional_offset: int = 0) -> str:
  """Return the python file's line number at which this function was called as a string, in the form 'filename:lineno'.

  Args:
    default: Any = None, will be returned if the function's calling place could not be determiend
    backtrack_frames: int = 1, how many frames to go back in the stack, if set to 1, will return the calling frame's line number, if set to 0 will return this module's internal line number (so dont) but may be useful when building a function that itself makes use of get_lineno() in which case you'd need to make it 2 so your function doesn't just return internal line number
    additional_offset: int = 0, since you cannot easily add to the stringified int, you may set this parameter to offset the returned line number by some amount.
  """

  frame = inspect.currentframe()
  for _ in range(backtrack_frames):
    if frame is None:
      raise RuntimeError('Invalid frame.')
    frame = frame.f_back

  return f'{frame.f_code.co_filename}:{get_lineno(default=default, backtrack_frames=backtrack_frames+1)+additional_offset}'


def get_pyversion_str(precision=2) -> str:
  return '.'.join([str(x) for x in sys.version_info[:precision]])
