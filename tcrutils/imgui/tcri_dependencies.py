def ensure_dependencies():
  MISSING_MODULES = []
  try:
    import imgui
    from imgui.integrations.glfw import GlfwRenderer
  except ModuleNotFoundError:
    MISSING_MODULES.append('imgui[glfw]')

  try:
    import glfw as gf
  except ModuleNotFoundError:
    MISSING_MODULES.append('glfw')

  try:
    import OpenGL.GL as gl
  except ModuleNotFoundError:
    MISSING_MODULES.append('PyOpenGL')

  try:
    import numpy as np
  except ModuleNotFoundError:
    MISSING_MODULES.append('numpy')

  if MISSING_MODULES:
    from ..src.tcr_console import console as c

    c.error('Please pip install the following modules for the GUI mode to work.')
    c.debug(*MISSING_MODULES, withprefix=False)
    raise RuntimeError('Missing modules.')
