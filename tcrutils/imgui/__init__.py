try:
  from .tcri_handler import ImGuiHandler
except ImportError:

  def ImGuiHandler(*_, **__):
    from ..src.tcr_console import console as __c

    msg1 = 'You need to install tcrutils with the [full] extra or [imgui] extra to use this module'
    msg2 = 'pip install tcrutils[imgui]'
    __c.error(msg1)
    __c.error(msg2)
    raise RuntimeError(f'{msg1}\n{msg2}')


from .tcri_utils import Every
from .types import tcri_types_imgui as imtypes
