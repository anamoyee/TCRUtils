import os


def _send(s: str) -> None:
  """Internal printhook."""
  print(s, end='')


class Cursor:
  def hide(self, *, return_code_only: bool = False) -> None | str:
    a = '\033[?25l'
    if return_code_only:
      return a
    else:
      _send(a)

  def unhide(self, *, return_code_only: bool = False) -> None | str:
    a = '\033[?25h'
    if return_code_only:
      return a
    else:
      _send(a)

class _TerminalSizeTuple(tuple):
  def __new__(cls, width: int, height: int):
    return super().__new__(cls, (width, height))

  def __init__(self, width: int, height: int) -> None:
    self.width = width
    self.height = height

  def __complex__(self):
    return complex(self.width, self.height)

  def __str__(self):
    return f'{self.width}x{self.height}'

class Terminal:
  @property
  def width(self):
    return os.get_terminal_size().columns

  @property
  def height(self):
    return os.get_terminal_size().lines

  @property
  def size(self):
    return _TerminalSizeTuple(*os.get_terminal_size())

  cursor = Cursor()

terminal = Terminal()

__all__ = ['terminal']
