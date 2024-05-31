from .tcr_ensure_deps import Dependency, DependencyEnsurer
from .tcr_terminal import terminal

ensure_dependencies = DependencyEnsurer(

)
"""Must be used before using any functions from this module."""

@terminal.hide_cursor_during_function
def menuconfig():
  """### Spawn a `make menuconfig`-styled menu.

  # Make sure to run `tcr.menuconfig.ensure_dependencies()` first!
  """
  return input('nya: ')
