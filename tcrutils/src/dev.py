"""Functions that are supposed to be run in development for example to generate a type hinter."""

import inspect
from types import FunctionType
from typing import Any

from .classfuncs import get_name_classname

print_ = print


def generate_function_argument_typehints(func: FunctionType) -> str:
	try:
		signature = inspect.signature(func)
	except ValueError:  # Signature not found
		return ""
	arguments_with_typehints = []
	for param in signature.parameters.values():
		if param.kind == inspect.Parameter.VAR_POSITIONAL:
			arguments_with_typehints.append("*" + param.name)
		elif param.kind == inspect.Parameter.VAR_KEYWORD:
			arguments_with_typehints.append("**" + param.name)
		else:
			argument = param.name
			if param.annotation != inspect.Parameter.empty:
				argument += f": {get_name_classname(param.annotation)}"
			if param.default == inspect.Parameter.empty:
				arguments_with_typehints.append(argument)
			else:
				arguments_with_typehints.append(f"{argument} = {param.default!r}")
	return ", ".join(arguments_with_typehints)


def generate_function_return_typehint(func: FunctionType) -> str:
	try:
		signature = inspect.signature(func)
	except ValueError:  # Signature not found
		return ""
	return_type = signature.return_annotation
	if return_type == inspect.Signature.empty:
		return ""
	else:
		return f" -> {get_name_classname(return_type)}"


def generate_type_hinter(
	obj: Any,
	/,
	*,
	clipboard: bool = False,
	print: bool = False,
	skip_leading_underscore: bool = False,
	attrib_whitelist: tuple[str] = (),
	attrib_blacklist: tuple[str] = ("sys", "os", "warnings"),
) -> str | None:
	"""Generates a string class definition for typehinting based on the object's dir() and the types of its attributes.

	Args:
	  obj (Any): The object to generate the type hint for.
	  clipboard (bool, optional): Whether to copy the result to the clipboard. Defaults to False. (Will also suppress any output to not flood the console)
	  print (bool, optional): Whether to print the result. Defaults to True. (Will also suppress any output to not flood the console)
	  skip_leading_underscore (bool, optional): Whether to skip leading underscores in the generated type hints. When False, skip only __double_leading_underscore (except some).
	  attrib_whitelist (tuple[str], optional): A tuple of attribute names to include in the type hint even if they don't match the specified `skip_leading_underscore` value (or none at all). Defaults to ().
	  attrib_blacklist (tuple[str], optional): A tuple of attribute names to exclude from the type hint no matter what. Defaults to ('sys', 'os').
	"""

	def sort_key(x):
		v = getattr(obj, x)
		if inspect.isclass(v):
			return 3
		if inspect.ismodule(v):
			return 2
		elif callable(v):
			return 1
		else:
			return 0

	hints = []
	processed_hints_dict = {}
	valid = (lambda x: not x.startswith("_")) if skip_leading_underscore else lambda x: not x.startswith("__")
	obj_dir = sorted([x for x in dir(obj) if ((valid(x)) or x in attrib_whitelist) and x not in attrib_blacklist], key=sort_key)
	for attr_name in obj_dir:
		attr_value = getattr(obj, attr_name)
		attr_type = get_name_classname(attr_value)
		if inspect.isclass(attr_value) or inspect.ismodule(attr_value):
			hints.append("\n  ".join(generate_type_hinter(attr_value).split("\n")))
		elif callable(attr_value):
			args_str = generate_function_argument_typehints(attr_value)
			hints.append(f"@staticmethod\n  def {attr_name}({args_str}){generate_function_return_typehint(attr_value)}: ...")
		else:
			hints.append(f"{attr_name}: {attr_type}")
		processed_hints_dict[attr_name] = attr_value

	if not obj_dir:
		hints.append("...")

	# hint types (imports)

	result = f"class {get_name_classname(obj).split('.')[-1]}:\n" + "\n".join(f"  {x}" for x in hints)

	if print:
		if callable(print):
			print(result)
		else:
			print_(result)

	if clipboard:
		from .console import console

		try:
			import pyperclip
		except ImportError:
			print("\npyperclip not installed. Installing...")
			import subprocess as __sp

			try:
				__sp.check_call(["pip", "install", "pyperclip"])
			except __sp.CalledProcessError:
				console.error("Unable to install pyperclip... Install it manually, returning without copy")
			else:
				import pyperclip

				pyperclip.copy(result)
				console.log(f"Copied to clipboard! ({len(result)} characters)")
			del __sp
		else:
			pyperclip.copy(result)
			console.log(f"Copied to clipboard! ({len(result)} characters)")

	if not (clipboard or print):
		return result
	else:
		return None
