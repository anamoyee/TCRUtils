from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import Any

import rich
from rich.markup import escape

from .extract_error import extract_error


def yay_print(
	obj: object,
	/,
	*objs: object,
	color: str = "yellow b",
	arrow: str = "==> ",
	arrow_color: str = "white b",
	escape_markup_obj: bool = True,
	escape_markup_objs: bool = False,
	sep: str = "",
	**kwargs,
):
	obj = str(obj)
	objs = tuple(str(s) for s in objs)

	if escape_markup_obj:
		obj = escape(obj)

	if escape_markup_objs:
		objs = tuple(escape(s) for s in objs)

	rich.print(f"[{arrow_color}]{arrow}[/][{color}]{obj!s}", *objs, sep=sep, **kwargs)


def nay_print(
	obj: object,
	*objs: object,
	color: str = "white b",
	arrow: str = "  -> ",
	arrow_color: str = "red b",
	**kwargs,
):
	return yay_print(obj, *objs, color=color, arrow=arrow, arrow_color=arrow_color, **kwargs)


def nay_print_e(
	e: BaseException,
	/,
	*objs: object,
	color: str = "magenta b",
	**kwargs,
):
	return nay_print(extract_error(e), *objs, color=color, **kwargs)


type _DictStrSelfOrListSelfOrStr = dict[str, _DictStrSelfOrListSelfOrStr] | list[_DictStrSelfOrListSelfOrStr] | str


def dictlist_to_markup(
	v: _DictStrSelfOrListSelfOrStr,
	*,
	escape_markup: bool = True,
) -> str:
	"""Convert a dict like the one below into str below below (in this docstr).

	```
	{"yellow": [
		"hello ",
		{"bold": "hello"},
		" world",
	]}
	```
	Gets converted into:
	```
	"[yellow]hello [bold]hello[/bold] world[/yellow]"
	```
	"""

	match v:
		case set():
			msg = "Do not use sets, since they're unordered unlike dicts in modern versions of python. Use list or tuple instead, or perhaps you meant to define a dict?"
			raise TypeError(msg)
		case str():
			if escape_markup:
				return escape(v)
			else:
				return v
		case _Mapping():
			return "".join(f"[{(keystripped := key.strip())}]{dictlist_to_markup(val, escape_markup=escape_markup)}[/{keystripped}]" for key, val in v.items())
		case _Iterable():
			return "".join(dictlist_to_markup(x, escape_markup=escape_markup) for x in v)

	raise TypeError(f"Expected T = dict[str, T] | list[T] | str, got: {v.__class__!r}")


if __name__ == "__main__":

	def __main():
		from tcrutils.console import c

		yay_print("yay print :3")
		yay_print("color='red i b s'", color="red i b s")

		print()
		nay_print("nay print 3:")

		print()
		nay_print_e(KeyError("asdf"), " <- idk")

		print()
		c ^ dictlist_to_markup(
			{
				"yellow": [
					"hello ",
					{"i": "hello", "b": "uwu"},
					" world",
				],
				"white": ("asdf", {"i": "owo"}, "nya"),
			},
		)

	__main()
