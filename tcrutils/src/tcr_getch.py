class _Getch:
  """Get a single character from standard input.

  Warning: May behave differently on Unix and Windows
  """

  def __init__(self):
    try:
      self.impl = _GetchWindows()
    except ImportError:
      self.impl = _GetchUnix()

  def __call__(self):
    """Get a single character from standard input.

    Warning: May behave differently on Unix and Windows
    """
    return self.impl()


class _GetchUnix:
  def __init__(self):
    import sys
    import termios
    import tty

    self.sys = sys
    self.termios = termios
    self.tty = tty

  def __call__(self):
    fd = self.sys.stdin.fileno()
    old_settings = self.termios.tcgetattr(fd)
    try:
      self.tty.setraw(self.sys.stdin.fileno())
      ch = self.sys.stdin.read(1)
    finally:
      self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)
    return ch.encode(encoding='ascii')


class _GetchWindows:
  def __init__(self):
    import msvcrt

    self.msvcrt = msvcrt

  def __call__(self):
    return self.msvcrt.getch()


getch = _Getch()
