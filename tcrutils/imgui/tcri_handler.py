import pathlib as p
from collections.abc import Callable
from sys import exit
from typing import ParamSpec, Self

try:
  import glfw as gf
  import imgui
  import OpenGL.GL as gl
  from imgui.integrations.glfw import GlfwRenderer
except ModuleNotFoundError:
  pass
else:

  def ctrlc_grace_exit() -> bool:
    print('^C', end='')
    return True  # Exit

  P = ParamSpec('P')

  class ImGuiHandler:
    frame: Callable[P, None]
    """The frame callback."""
    title: str
    """The title of the window."""
    font_path: p.Path | None
    """The path to the font file to use, or None to disable."""
    ctrlc_handler: Callable[[], bool]
    """The Ctrl-C handler to use. Return True to exit the gui, False to continue. Do not exit()."""

    def __init__(self):
      self.title = 'Untitled window'
      self.font_path = None
      self.ctrlc_handler = ctrlc_grace_exit
      self.start_maximised = False

    def set_title(self, title: str = 'Untitled window') -> Self:
      if not isinstance(title, str):
        raise TypeError('title must be str')
      self.title = title
      return self

    def set_font_path(self, font_path: p.Path | str | None = None) -> Self:
      if isinstance(font_path, str):
        font_path = p.Path(font_path)
      if font_path is not None and not isinstance(font_path, p.Path):
        raise TypeError('font_path must be str or pathlib.Path (or None to disable)')
      if font_path is not None and not font_path.is_file():
        raise FileNotFoundError(f"font_path {font_path} doesn't exist or is not a file")
      self.font_path = font_path
      return self

    def set_ctrlc_handler(self, ctrlc_handler: Callable[[], bool] = ctrlc_grace_exit) -> Self:
      if ctrlc_handler is not None and not callable(ctrlc_handler):
        raise TypeError('ctrlc_handler must be Callable[[], bool]')
      self.ctrlc_handler = ctrlc_handler
      return self

    def set_start_maximised(self, start_maximised: bool = False) -> Self:
      self.start_maximised = start_maximised
      return self

    def __call__(self, frame: Callable[P, None], /):
      self.frame = frame
      return self

    def run(self, *args: P.args, **kwargs: P.kwargs) -> None:
      self.args = args
      self.kwargs = kwargs
      imgui.create_context()
      if not gf.init():
        raise RuntimeError('Could not initialize OpenGL context')

      gf.window_hint(gf.CONTEXT_VERSION_MAJOR, 3)
      gf.window_hint(gf.CONTEXT_VERSION_MINOR, 3)
      gf.window_hint(gf.OPENGL_PROFILE, gf.OPENGL_CORE_PROFILE)
      gf.window_hint(gf.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

      window = gf.create_window(*gf.get_monitor_physical_size(gf.get_primary_monitor()), self.title, None, None)
      gf.make_context_current(window)

      if not window:
        gf.terminate()
        raise RuntimeError('Could not initialize GLFW window.')

      if self.start_maximised:
        gf.maximize_window(window)

      impl = GlfwRenderer(window)

      io = imgui.get_io()
      jb = io.fonts.add_font_from_file_ttf(self.font_path, 30) if self.font_path is not None else None
      impl.refresh_font_texture()

      while not gf.window_should_close(window):
        try:
          self._render(impl, window, jb)
        except KeyboardInterrupt:
          if self.ctrlc_handler():
            break

      impl.shutdown()
      gf.terminate()

    def _render(self, impl, window, font):
      gf.poll_events()
      impl.process_inputs()
      imgui.new_frame()

      gl.glClearColor(0.1, 0.1, 0.1, 1)
      gl.glClear(gl.GL_COLOR_BUFFER_BIT)

      if font is not None:
        imgui.push_font(font)

      self.frame(*self.args, **self.kwargs)

      if font is not None:
        imgui.pop_font()

      imgui.render()
      impl.render(imgui.get_draw_data())
      gf.swap_buffers(window)
