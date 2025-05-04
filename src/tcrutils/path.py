import inspect
import os
import pathlib as p
import re
from collections.abc import Callable


def convert_to_relative_path(
	absolute_path: str | p.Path,
	relative_to: str | p.Path | None = None,
) -> p.Path:
	"""Convert absolute path into a relative path, if not possible, return the absolute path."""
	relative_to = relative_to if relative_to is not None else p.Path.cwd()

	absolute_path = p.Path(absolute_path)

	try:
		relative_path = absolute_path.relative_to(relative_to)
	except ValueError:
		return str(absolute_path)

	return p.Path() / relative_path


def convert_to_relative_pathstr(
	absolute_path: str | p.Path,
	relative_to: str | p.Path | None = None,
	*,
	consistent_slashes: bool = True,
) -> str:
	"""Convert absolute path into a relative path string, if not possible, return the absolute path string."""
	converted = convert_to_relative_path(absolute_path=absolute_path, relative_to=relative_to)
	converted = str(converted)

	if consistent_slashes and os.name == "nt":
		converted = converted.replace("\\", "/")

	if any(converted.startswith(x) for x in ("\\", "/")):
		return converted

	if os.name == "nt" and ":" in converted:
		return converted

	return f".{'\\' if (os.name == 'nt' and not consistent_slashes) else '/'}{converted}"


def nextname(name="New folder") -> str:
	"""### If passed in name does not end with "`({int})" where `{int}` is any integer, return it with "` (1)`" appended else return it with the previously mentioned `{int}` incremented and leave it otherwise unchanged."""
	match = re.match(r"^(.*) \((\d+)\)$", name)

	if match:
		base_name = match.group(1)
		current_index = int(match.group(2))
		new_name = f"{base_name} ({current_index + 1})"
	else:
		new_name = f"{name} (1)"

	return new_name


def nextname_file_ext_fix(name="New file.txt") -> str:
	match = re.match(r"^(.*?)(?:\s*\((\d+)\))?(?:\.(\w+))?$", name)
	if not match:
		raise ValueError("Invalid filename format")

	base_name, number, extension = match.groups()

	new_number = int(number) + 1 if number else 1

	return f"{base_name} ({new_number}).{extension}" if extension else f"{base_name} ({new_number})"


def get_unused_dirname(
	name: str | None = None,
	path: p.Path | str | None = None,
	nextname: Callable[[str | None], str] = nextname,
) -> str:
	"""Return unused directory or file with the name `name` in directory `path` or the current directory if not passed in."""
	if path is None:
		path = os.getcwd()
	path = str(path)
	listdir = os.listdir(path)
	while name in listdir:
		name = nextname(name)
	return name


def pyrootfile() -> p.Path:
	"""Return the file from which the python code execution originated, furthest back in the callstack as pathlib.Path."""
	return p.Path(inspect.stack()[-1].filename)


def pyrootdir() -> p.Path:
	"""Return the directory of the furthest back file in the callstack as pathlib.Path."""
	return pyrootfile().parent


if True:  # isreserved
	nt_reserved_chars = frozenset({chr(i) for i in range(32)} | {'"', "*", ":", "<", ">", "?", "|", "/", "\\"})

	nt_reserved_names = frozenset({"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {f"COM{c}" for c in "123456789\xb9\xb2\xb3"} | {f"LPT{c}" for c in "123456789\xb9\xb2\xb3"})

	def isreserved(path: str | p.Path, *, strict: bool = True) -> bool:
		"""Return true if the pathname is reserved by the system.

		Part backport of Py3.13's os.path.isreserved() and also works on Linux (probably).

		Args:
			strict: If true, mark some more paths as reserved on Windows, on Linux no effect.
		"""

		path = str(path)

		if os.name != "nt":
			return "\x00" in path

		if strict:
			if path.startswith(" "):
				return True

		from os.path import altsep, sep, splitroot

		# Refer to "Naming Files, Paths, and Namespaces":
		# https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
		path = os.fsdecode(splitroot(path)[2]).replace(altsep, sep)
		return any(_isreservedname(name) for name in reversed(path.split(sep)))

	def _isreservedname(name):
		"""Return true if the filename is reserved by the system."""
		# Trailing dots and spaces are reserved.
		if name[-1:] in (".", " "):
			return name not in (".", "..")
		# Wildcards, separators, colon, and pipe (*?"<>/\:|) are reserved.
		# ASCII control characters (0-31) are reserved.
		# Colon is reserved for file streams (e.g. "name:stream[:type]").
		if nt_reserved_chars.intersection(name):
			return True
		# DOS device names are reserved (e.g. "nul" or "nul .txt"). The rules
		# are complex and vary across Windows versions. On the side of
		# caution, return True for names that may not be reserved.
		return name.partition(".")[0].rstrip(" ").upper() in nt_reserved_names
