try:
	from .handler import ImGuiHandler
except ImportError:

	def ImGuiHandler(*_, **__):
		from ..console import console as __c

		msg1 = "You need to install tcrutils with the [full] extra or [imgui] extra to use this module"
		msg2 = "pip install tcrutils[imgui]"
		__c.error(msg1)
		__c.error(msg2)
		raise RuntimeError(f"{msg1}\n{msg2}")


from .types import imgui as imtypes
from .utils import Every
