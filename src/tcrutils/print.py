import ast
import datetime as dt
import pathlib
import re as regex
import string
import sys
import typing
from _collections_abc import (
	Callable,
	ItemsView,
	Iterable,
	KeysView,
	Mapping,
	ValuesView,
	bytearray_iterator,
	bytes_iterator,
	coroutine,
	dict_itemiterator,
	dict_items,
	dict_keyiterator,
	dict_keys,
	dict_valueiterator,
	dict_values,
	list_iterator,
	list_reverseiterator,
	longrange_iterator,
	range_iterator,
	set_iterator,
	str_iterator,
	tuple_iterator,
	zip_iterator,
)
from enum import Enum, EnumMeta
from functools import partial, wraps
from json import dumps as _json_dumps
from json import loads as _json_loads
from types import GeneratorType, UnionType
from typing import Any
from typing import get_args as unpack_union
from warnings import warn

from colored import Back, Fore, Style

from .compare import able, able_simple, able_simple_result
from .dict import clean_dunder_dict
from .extract_error import extract_error
from .int import hex as tcrhex
from .iterable import Or, getattr_queue, limited_iterable
from .path import convert_to_relative_pathstr
from .types import BrainfuckCode, GayString, QuotelessString

_HikariEnum = None
PydanticBM = None

# def double_quoted_repr(s: str, *, quote_char: str = '"'):
# 	"""Return a string that is the same as `s` but always uses `quote_char` instead of single or double quotes on string boundaries. Make sure to correctly escape every character if needed so there are no edge cases that might break the result."""
# 	assert quote_char in ('"', "'")
# 	result = quote_char
# 	for char in s:
# 		if char in "\\" + quote_char:
# 			result += "\\" + char
# 		else:
# 			result += char
# 	return result + quote_char

# fuck this shit, json dumps exists
# https://tenor.com/en-GB/view/faktycznie-ok-dobra-drake-gif-25333966


def _regex_replace_u(m: regex.Match):
	rest = _json_loads(f'"{m.group(2)}"')

	return repr(f"{m.group(1) or ''}{rest}")[1:-1]


def repr_if_needed(
	s: str,
	*,
	syntax_highlighting=True,
	quoteless=False,
	no_implicit_quoteless=False,
) -> str:
	dumped = _json_dumps(s)

	# fmt: off
	subs = (
		(r"(?<!\\)(\\\\)*\\u0000(?![0-9])",      r"\1\\0"),
		(r"(?<!\\)(\\\\)*\\u00([a-z0-9]{2})",    r"\1\\x\2"),
		(r"(?<!\\)(\\\\)*((?:\\u[a-z0-9]{4})+)", _regex_replace_u), # Commented out - possibly better to leave things as they are - with \u's instead of 񂍆 񂍆 񂍆
	)
	# fmt: on

	for pat, sub in subs:
		dumped = regex.sub(pat, sub, dumped)

	if not syntax_highlighting:
		return dumped

	if quoteless or (not no_implicit_quoteless and regex.match(r'"[a-zA-Z0-9_]+"', dumped)):
		return f"{FMTC.STRING}{dumped[1:-1]}{FMTC._}"
	else:
		return f"{FMTC.QUOTES}{dumped[0]}{FMTC.STRING}{dumped[1:-1]}{FMTC.QUOTES}{dumped[-1]}{FMTC._}"


def print_block(
	text: str,
	border_char: str = "#",
	*,
	margin: int = 1,
	border: int = 3,
	padding: int = 0,
	padding_top: int = 1,
	padding_bottom: int = 1,
	text_color: str = Fore.YELLOW + Style.bold,
	border_color: str = Fore.WHITE + Style.bold,
	raw: bool = False,
	allow_invalid_config: bool = False,
) -> str | None:
	"""Print or return a string of a "comment-like" block with text. Colors may optionally be set to `''` (empty string) to skip coloring of that part. Ends with a color reset unless none of the colors are enabled (both set to `''`).

	Params:
	                - `margin`: The amount of spaces between the text and the inner walls (left-right only)
	                - `border`: The width of walls (number of border_char characters, left-right only)
	                - `padding`: The number of extra spaces added to the left of each line (left side only)
	                - `padding_top` & `padding_bottom`: How many '\\n' characters to add at the beginning and the end of the string (top-bottom only)
	"""

	text = str(text)

	if (not allow_invalid_config and margin < 0) or border < 0 or padding < 0:
		msg = f"Invalid margin, border and/or padding(s) configuration {(margin, border, padding, padding_top, padding_bottom)!r}. Override this by passing in allow_invalid_config=True"
		raise ValueError(msg)

	if not allow_invalid_config and len(border_char) != 1:
		msg = f"border_char must be 1 character long (got {border_char!r} which is {len(border_char)!r} characters long). Override this by passing in allow_invalid_config=True"
		raise ValueError(msg)

	reset = Style.reset

	if not text_color and not border_color:
		reset = ""

	bar = f"{border_char * (border + margin + len(text) + margin + border)}"
	block = f"""
{padding_top * "\n"}{padding * " "}{reset}{border_color}{bar}
{padding * " "}{border * border_char}{reset}{margin * " "}{text_color}{text}{reset}{margin * " "}{border_color}{border * border_char}
{padding * " "}{bar}{reset}{padding_bottom * "\n"}
"""[1:-1]
	if raw:
		return block

	print(block)
	return None


if True:  # \/ # fmt & print iterable
	# fmt: off
	# Format Colors, name kept short so lines don't get THAT long if this thing is used like 10 times in a single fstring
	class FMTC:
		_                   = Style.reset # Reset
		bold                = Style.bold

		NUMBER              = Fore.LIGHT_BLUE + Style.bold
		NUMBER_NO_BOLD      = _ + Fore.LIGHT_BLUE
		TYPE                = Fore.LIGHT_BLUE + Style.bold
		DECIMAL             = Fore.WHITE + Style.bold
		DECIMAL_NO_BOLD     = _ + Fore.WHITE
		BRACKET             = Fore.CYAN + Style.bold
		ENUM_VARIANT_NAME   = _ + Fore.WHITE # Reset for no bold
		QUOTES              = _ + Fore.WHITE # Reset for no bold
		STRING              = _ + Fore.YELLOW # Reset for no bold
		COLON               = Fore.WHITE + Style.bold # Sorry, no 0xFF8000 gdcolon color, it looked too smushed together with the string color when in a dict {a: b};   = Fore.orange_1 + Style.bold
		GD_COLON            = Fore.ORANGE_1 + Style.bold # NEVERMIND THE ABOVE i actually need the color for at least one thing so here it is back..
		ASTERISK            = Fore.ORANGE_1 + Style.bold
		COROUTINE           = Fore.ORANGE_1 + Style.bold
		FUNCTION            = Fore.ORANGE_1 + Style.bold
		COMPLEX             = Fore.ORANGE_1 + Style.bold
		COMMA               = Fore.DARK_GRAY + Style.bold
		COMMA_NO_BOLD       = _ + Fore.DARK_GRAY
		PIPE                = Fore.DARK_GRAY + Style.bold
		PATH_SLASH          = DECIMAL
		UNKNOWN             = Fore.DARK_GRAY + Style.bold
		TRUE                = Fore.LIGHT_GREEN + Style.bold
		FALSE               = Fore.LIGHT_RED + Style.bold
		UNDEFINED           = Fore.DARK_GRAY + Style.bold
		NONE                = Fore.LIGHT_GRAY + Style.bold
		BYTESTR_B           = Fore.RED + Style.bold
		ITER_I              = Fore.red_3b + Style.bold
		SPECIAL             = Fore.purple_1b + Style.bold
		INTERNAL_EXCEPTION  = Fore.red_3b + Style.bold
		BUILT_IN_EXCEPTION  = Fore.BLUE + Style.bold
		MODULE              = Fore.ORANGE_1 + Style.bold

		def __call__(self): # If called FMTC() then passed instance as FMTC= kwarg, then another piece of code makes another instance thus FMTC()() effectively
			return self

	class FMT_LETTERS:
		b    = f'{FMTC.BYTESTR_B}b'
		i    = f'{FMTC.ITER_I}i{FMTC._}'
		F    = f'{FMTC.SPECIAL}F'
		K    = f'{FMTC.SPECIAL}K'
		V    = f'{FMTC.SPECIAL}V'
		I    = f'{FMTC.SPECIAL}I'
		C    = f'{FMTC.COROUTINE}C'
		META = f'{FMTC.SPECIAL}Meta'

	# Format Brackets templates.
	# (FMT_BRACKETS[_t][syntax_highlighting: bool] % content) -> attaches brackets to the content with respect to syntax highlighting
	FMT_BRACKETS: dict[type | None, tuple[str, str]] = { # Format Brackets
		None:          ('[%s]',            f'{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		list:          ('[%s]',            f'{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		dict_keys:     ('[%s]',            f'{FMT_LETTERS.K}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		dict_values:   ('[%s]',            f'{FMT_LETTERS.V}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		dict_items:    ('[%s]',            f'{FMT_LETTERS.I}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		KeysView:      ('[%s]',            f'{FMT_LETTERS.K}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		ValuesView:    ('[%s]',            f'{FMT_LETTERS.V}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		ItemsView:     ('[%s]',            f'{FMT_LETTERS.I}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		set:           ('{%s}',            f'{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
		frozenset:     ('frozenset({%s})', f'{FMT_LETTERS.F}{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
		dict:          ('{%s}',            f'{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
		Mapping:       ('{%s}',            f'{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
		tuple:         ('(%s)',            f'{FMTC.BRACKET}({FMTC._}%s{FMTC.BRACKET}){FMTC._}'),
		GeneratorType: ('[%s]',            f'{FMTC.BRACKET}<{FMTC._}%s{FMTC.BRACKET}>{FMTC._}'),
		range:         ('range([%s])',     f'{FMTC.BRACKET}<{FMTC._}%s{FMTC.BRACKET}>{FMTC._}'),
		bytearray:     ('bytearray([%s])', f'{FMT_LETTERS.b}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
		coroutine:     ('coroutine_%s',    f'{FMT_LETTERS.C}{FMTC.DECIMAL}\'{FMTC.FUNCTION}%s')
	}

	FMT_TOO_DEEP = ('[ ... ]', f'{FMTC.BRACKET}[ {FMTC.DECIMAL}... {FMTC.BRACKET}]{FMTC._}')

	FMT_RECURSIVE_STRUCTURE_SEEN = ('[[ ... ]]', f'{FMTC.BRACKET}[[ {FMTC.SPECIAL}... {FMTC.BRACKET}]]{FMTC._}')

	FMT_UNION_SEPARATOR = ('|', f'{FMTC.PIPE} | {FMTC._}')

	FMT_ITER = ('iter(%s)', f'{FMT_LETTERS.i}%s')

	FMT_UNKNOWN = ('%s(%s)', f'{FMTC.UNKNOWN}%s({FMTC._}%s{FMTC.UNKNOWN}){FMTC._}')
	FMT_UNKNOWN_NO_PARENS = ('%s%s', f'{FMTC.UNKNOWN}%s{FMTC._}%s{FMTC._}')
	FMT_UNKNOWN_ADDRESS = ('%s@%s', f'{FMTC.UNKNOWN}%s{FMTC.DECIMAL}@{FMTC._}%s{FMTC._}')
	FMT_UNKNOWN_ADDRESS_WITH_CALL = ('%s@%s(%s)', f'{FMTC.UNKNOWN}%s{FMTC.DECIMAL}@{FMTC._}%s{FMTC.UNKNOWN}({FMTC._}%s{FMTC.UNKNOWN}){FMTC._}')

	FMT_INTERNAL_EXCEPTION = ("An exception occured while trying to display this item (%s).", f"{FMTC.INTERNAL_EXCEPTION}An exception occured while trying to display this item ({FMTC.UNKNOWN}%s{FMTC.INTERNAL_EXCEPTION}).{FMTC._}")

	FMT_CLASS = ("%s(%s)", f"{FMTC.TYPE}%s{FMTC.BRACKET}({FMTC._}%s{FMTC.BRACKET}){FMTC._}")

	FMT_ENUM_VARIANT = ('%s.%s=%s', f'{FMTC.TYPE}%s{FMTC.COMMA}.{FMTC._}%s{FMTC.COMMA}: {FMTC._}%s')

	FMT_ENUM_VARIANT_NO_CLASS = ('%s=%s', f'{FMTC._}%s{FMTC.COMMA}: {FMTC._}%s')

	FMT_ENUM_VARIANT_AUTO = ('%s.%s', f'{FMTC.TYPE}%s{FMTC.COMMA}.{FMTC._}%s')

	FMT_ENUM_VARIANT_AUTO_NO_CLASS = ('%s', f'{FMTC._}%s')

	FMT_ASTERISK = ('*', f'{FMTC.ASTERISK}*')

	FMT_SYS_VERSION_INFO = f'{FMTC.GD_COLON}Python%s'

	# fmt: on

	class _OverflowClass:
		amount: int

		def __init__(self, amount) -> None:
			self.amount = amount

		def __str__(self) -> str:
			return str(self.amount) if self.amount != -1 else "?"

	def _is_date_in_the_past(input_dt: dt.datetime | dt.date | dt.time) -> bool:
		if isinstance(input_dt, dt.datetime):
			return (dt.datetime.now(tz=input_dt.tzinfo) - input_dt).total_seconds() > 5  # Assume 5s margin of error
		elif isinstance(input_dt, dt.date):
			return input_dt < dt.date.today()  # noqa: DTZ011 <- Cannot obrain a good timezone, if i were to obtain the computer's, that's no differnet than today() obtaining time from time.time(), right?
		elif isinstance(input_dt, dt.time):
			now_time = dt.datetime.now(tz=input_dt.tzinfo).time()
			then_total_seconds = input_dt.hour * 3600 + input_dt.minute * 60 + input_dt.second
			now_total_seconds = now_time.hour * 3600 + now_time.minute * 60 + now_time.second
			return now_total_seconds - then_total_seconds > 5

		raise TypeError("input must be either datetime, date or time")

	def _reset_return_wrapper(func):
		@wraps(func)
		def wrapper(*args, append_syntax_reset: bool = True, **kwargs):
			return func(*args, **kwargs)  # Disabled due to it kind of really slowing down performance, may be re-enabled later if i want idk......
			if kwargs.get("syntax_highlighting") and append_syntax_reset:
				s = f"{FMTC._}{func(*args, **kwargs)}{FMTC._}"

				for v in vars(FMTC).values():  # Clear any duplicate, side-by-side color tags.
					if not isinstance(v, str):
						continue

					_2v = 2 * v
					while _2v in s:
						s = s.replace(_2v, v)

				return s
			return func(*args, **kwargs)

		return wrapper

	def _non_double_repr(obj: object, /) -> str:
		rep = repr(obj)

		if not rep:
			return rep

		if not hasattr(obj, "__class__"):
			return rep

		if not hasattr(obj.__class__, "__name__"):
			return rep

		if rep.removeprefix(obj.__class__.__name__) == rep:
			return rep

		if not rep.removeprefix(obj.__class__.__name__):
			return ""

		if rep.removeprefix(obj.__class__.__name__)[0] != "(":
			return rep

		if rep[-1] != ")":
			return rep

		return rep[(len(obj.__class__.__name__) + 1) : -1]

	def _is_enum_auto(enum_class: EnumMeta) -> bool:
		"""Whether enum seems to be made with all variants `= auto()`.

		If the values are all ints and they are in either of the patterns:
		- [1, 2, 3, ...] (each number is 1 more than the previous, starting at 1)
		- [1, 2, 4, 8, 16, ...] (each number is a consecutive power of 2 (for example the idx=0 element must be 2**0 and idx=1 must be 2**1, etc.), starting at 1)

		...If any of those patterns match, the enum is considered being made with `auto()`
		"""

		variants = list(enum_class)

		values = [x.value for x in variants]

		if all(x == i for i, x in enumerate(values)):
			return True

		if all(x == (i + 1) for i, x in enumerate(values)):
			return True

		return bool(all(x == 2**i for i, x in enumerate(values)))

	def _fmt_enum_variant_name(name: str, syntax_highlighting: bool) -> str:
		if not syntax_highlighting:
			return name

		return f"{FMTC.ENUM_VARIANT_NAME}{name.replace('|', f'{FMTC.COMMA}|{FMTC.ENUM_VARIANT_NAME}')}"

	def _fmt_module_highlighted(name: str, path: str | None, namespace: str | None) -> str:
		s = f"{FMTC.MODULE}{name}"
		if namespace:
			s += FMT_BRACKETS[tuple][True] % f"{FMTC.MODULE}{namespace}"
		if path:
			path = path.replace("\\\\", "\\")
			if "/" not in path:
				path = path.replace("\\", "/")
			path = fmt_iterable(path if " " in path else QuotelessString(path), syntax_highlighting=True)
			s += f"{FMTC.DECIMAL}@{path}"
		return s

	def _fmt_unknown_highlighted(it: object, /, queue_name: str, *, this) -> str:
		repr_it = repr(it)

		if match := regex.match(
			r"<module '(?P<module_name>[^']+)'(?: from '(?P<path>[^']+)')?(?: \((?P<namespace>[^)]+)\))?>",
			repr_it,
		):
			d = match.groupdict()

			name = d["module_name"]
			path = d["path"]
			if path is not None:
				path = convert_to_relative_pathstr(path)
			namespace = d["namespace"]

			return _fmt_module_highlighted(name, path, namespace)
		elif match := regex.match(
			r"<([a-zA-Z_ ]+) at 0x([0-9a-zA-Z]{8,})(?:: )?(.*)>",
			repr_it,
		):
			name, address_str, rest = match.groups()

			allowed_chars = string.ascii_letters + string.digits + "_"

			name_fmted = name if all((ch in allowed_chars) for ch in name) else this(name).replace(FMTC.STRING, FMTC.UNKNOWN)

			address_fmted = this(int(address_str, base=16))

			return FMT_UNKNOWN_ADDRESS_WITH_CALL[True] % (name_fmted, address_fmted, rest)

		elif match := regex.match(
			r"^([^\d\W](?:(?:\w)|(?:\.<locals>\.)|(?:\.<globals>\.))*)\((.*)\)$",
			repr_it,
		):
			name, body = match.groups()

			return FMT_UNKNOWN[True] % (name, body)
		else:
			return FMT_UNKNOWN[True] % (
				queue_name,
				_non_double_repr(it),
			)

	def _fmt_brainfuck(text: BrainfuckCode) -> str:
		"""Format a string as brainfuck.

		Assuming syntax_highlighting==True && isinstance(text, BrainfuckCode)
		"""
		return str(
			text.replace("[", "#")
			.replace("<", f"{FMTC.ASTERISK}<")
			.replace(">", f"{FMTC.ASTERISK}>")
			.replace(".", f"{FMTC.DECIMAL}.")
			.replace(",", f"{FMTC.COMMA},")
			.replace("+", f"{FMTC.TRUE}+")
			.replace("-", f"{FMTC.FALSE}-")
			.replace("]", f"{FMTC.BRACKET}]")
			.replace("#", f"{FMTC.BRACKET}[")
		)

	def _pydantic_hopefully_non_erroring_dumper(obj) -> dict:
		return {k: getattr(obj, k) for k in obj.__class__.model_fields}

	def parse_repr_literal(repr_str: str) -> tuple[str, tuple[Any], dict[str, Any]]:
		"""Parse a repr in the form of Class('args', 'args', ..., kwargs='kwargs', kwargs2=2) and return ParsedRepr(name='Class', args=('args', 'args', ...), kwargs={'kwargs': 'kwargs', 'kwargs2': 2}). Fail with ValueError on non-literal parsing.

		Raises:
		        ValueError: Parsing failed
		        TypeError: repr_str is not a str
		"""
		try:
			if not isinstance(repr_str, str):
				raise TypeError("repr_str must be a str.")

			node = ast.parse(repr_str, mode="eval")

			if not isinstance(node.body, ast.Call):
				raise ValueError("Not a valid function call format.")  # noqa: TRY004

			if isinstance(node.body.func, ast.Name):
				name = node.body.func.id  # Something(...)
			elif isinstance(node.body.func, ast.Attribute):
				# Build full qualified name inline
				name_parts = []
				current_node = node.body.func
				while isinstance(current_node, ast.Attribute):
					name_parts.append(current_node.attr)
					current_node = current_node.value
				if isinstance(current_node, ast.Name):
					name_parts.append(current_node.id)
				else:
					raise ValueError("Invalid callable.")  # noqa: TRY004
				name = ".".join(reversed(name_parts))
			else:
				raise ValueError("Invalid callable.")  # noqa: TRY004

			args = []
			for arg in node.body.args:
				try:
					args.append(ast.literal_eval(arg))  # Ensure it's a literal
				except ValueError:
					raise ValueError(  # noqa: B904
						f"Invalid literal in positional args: {ast.dump(arg)}"
					)

			kwargs = {}
			for kwarg in node.body.keywords:
				if not isinstance(  # noqa: UP038
					kwarg.value, (ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set)
				):
					raise ValueError(f"Invalid literal in keyword args: {kwarg.arg}")  # noqa: TRY004
				kwargs[kwarg.arg] = ast.literal_eval(kwarg.value)

			return (name, tuple(args), kwargs)

		except ValueError:
			raise
		except Exception as e:
			raise ValueError(e)  # noqa: B904

	def load_dynamic_modules_if_needed():
		global _HikariEnum, PydanticBM

		if "hikari.internal.enums" in sys.modules:
			from hikari.internal.enums import Enum as _HikariEnum

		if "pydantic" in sys.modules:
			from pydantic import BaseModel as PydanticBM

	load_dynamic_modules_if_needed()  # Try to find dynamic modules and load them at load time, not to slow down the query time, though it might not be possible if the import order is fucked

	def fmt_iterable(
		it: Iterable | Any,
		/,
		*its: Iterable | Any,
		indentation: int = 4,
		item_limit: int = 100,
		depth_limit: int = 100,
		syntax_highlighting: bool = False,
		trailing_commas: bool = True,
		int_formatter: Callable[[int], str] | None = None,
		let_no_indent: bool = True,
		force_no_indent: int = 0,
		force_no_spaces: bool = False,
		force_complex_parenthesis: bool = False,
		force_slice_parenthesis: bool = False,
		force_union_parenthesis: bool = True,
		prefer_full_names: bool = False,
		str_repr: Callable[[str], str] = repr_if_needed,
		prefer_pydantic_better_dump: bool = False,
		FMTC=FMTC,
		**kwargs,
	) -> str:
		"""### Return iterable as formatted string with optional syntax highlighting.

		This also supports primitive types to be included in the iterables although passing primitive types themselves is fine.

		For printing the iterable use tcr.print_iterable().\\
		For debugging use tcr.console().

		Example:
		```py
		>>> fmt_iterable([10, 20, 30])
		'[\\n  10,\\n  20,\\n  30,\\n]'
		>>> fmt_iterable({10: 20, 30: 40})
		'{\\n  10: 20,\\n  30: 40,\\n}'
		```

		Args:
			it: Iterable, The iterable to format
			*its: Iterable, The same as above, if provided, it = (it, *its), can be omitted.
			indentation: int, How many spaces between where the list bracket is placed and the list items.
			item_limit: int, How many items in a list can be displayed before it's cut off. Any values < 1 will be set back to 1
			syntax_highlighting: bool, Whether or not terminal color codes should be added to make the code/iterables perttier. This also slightly changes the syntax. For example `'{,}'` with syntax highlighting and `'set()'` without. If you wish to copy & paste the iterable from terminal back to code set this to False although it may work with it set to true as well. The extra syntax safety does not support generators and `"(X more items...)"` messages that come from `item_limit`.
			trailing_commas: bool, whether or not to add trailing commas to lists (`'[\\n  10,\\n  20,\\n]'` vs `'[\\n  10,\\n  20\\n]'`). Psst: this can be set to 2 to force trailing commas although it's not recommended to use this as a feature.
			int_formatter: Callable[[int], str], A function that formats integers to a string. For example tcr.hex will format all integers as hex values. The tcr.hex formatter is automatically used unless other one was supplied
			let_no_indent: bool, Let the function automatically determine good spots to remove excessive enter-indent-syntax (for example "[\\n  10,\\n  20\\n]" - The list has only two, non iterable items or when the list has only one iterable or non iterable item)
			force_no_indent: bool, Force the condition above (let_no_spaces), skip any conditions listed there, never add extra enters or indents even if it may make the result unreadable. This effectively makes `indent` or `let_no_indent` irrelevant. This also sets `trailing_commas` to False.
			force_no_spaces: bool, Force remove any extra spaces (not including the objects' values for example strings will still be displayed with spaces). It removes spaces for example after commas, colons, etc. This effectively enables `force_no_indent` thus making `indent` or `let_no_indent` irrelevant.
			force_complex_parenthesis: bool, Force parenthesis when displaying `complex` type for example `(3 + 1j)` instead of `3+1j`. This has no effect when syntax highlighting is turned off.
			force_slice_parenthesis: bool, Force parenthesis when displaying `slice` type for example `(::-1)` instead of `::-1`. This has no effect when syntax highlighting is turned off.
			force_union_parenthesis: bool, Force parenthesis when displaying `union` type.` This has no effect when syntax highlighting is turned off.
			prefer_full_names: bool, whether or not to use the full names of objects if possible.
			let_no_indent_max_iterables: int = 1, (advanced) override the limit for iterables for the let_no_indent feature
			let_no_indent_max_non_iterables: int = 4, (advanced) override the limit for non-iterables for the let_no_indent feature
			str_repr: Callable[[str], str] = json_dumps, (advanced) override the default string repr callable
			prefer_pydantic_better_dump: bool = False, Will use the pydantic's custom dumper which prints the model name in more places, instead of leaving it only for the moment when pydantic SHITS ITS PANTS (raises random shitass errors). i have nothing more to say about this.

		If no formatting is set for an object, it can be defined using the __tcr_display__(self, **kwargs) or __tcr_fmt__(self, *, fmt_iterable, **kwargs) methods.

		```py
		class PrintableObj:
		def __tcr_display__(self=None, **kwargs) -> str:
			return 'tcr.fmt-able object' + ('\'s instance' if self is not None else '')

		>>> fmt_iterable([PrintableObj])
		'tcr.fmt-able object'
		>>> fmt_iterable([PrintableObj()])
		"tcr.fmt-able object's instance"
		```
		"""
		if depth_limit < 0:
			depth_limit = 0
		if kwargs.get("__depth", 0) > depth_limit:
			return FMT_TOO_DEEP[syntax_highlighting]

		if id(it) in kwargs.get("__seen", {}):
			return FMT_RECURSIVE_STRUCTURE_SEEN[syntax_highlighting]

		if its:
			it = [it, *its]

		item_limit = int(item_limit)
		if item_limit < 0:
			item_limit = 1

		is_iterable = able_simple(isinstance, it, Iterable) and isinstance(it, Iterable)
		is_mapping = able_simple(isinstance, it, Mapping) and isinstance(it, Mapping)

		if (
			# if this feature is turned on:
			let_no_indent
			and not force_no_spaces
			# for all Iterables...
			and is_iterable
			# ...that don't have already hardcoded displays
			and not isinstance(it, str | bytes)
			# If their length can be checked (e.g. not generators)
			and able_simple(len, it)
			# And they have any length:
			and len(it) > 0
			# And none of the items inside have a __tcr_fmt__ because reasons
			and not any(hasattr(x, "__tcr_fmt__") for x in it)
		):
			if is_mapping:
				if len(it) == 1:
					force_no_indent = -1
			else:
				# Case 1: If the iterable in question contains iterables
				# If there is at most 1 iterable in the outer iterable of iterables
				if len(it) <= Or(kwargs.get("let_no_indent_max_iterables"), 1) and any(isinstance(x, Iterable) for x in it):
					force_no_indent = -1
				# Case 2: If the outer iterable consists of non-iterables: If there are at most 4 non-iterables
				if all((not isinstance(x, Iterable)) or isinstance(x, str | bytes) or (able(len, x) and len(x) == 0) for x in it) and len(it) <= Or(kwargs.get("let_no_indent_max_non_iterables"), 4):
					force_no_indent = -1

		name = "__qualname__" if prefer_full_names else "__name__"
		space = " " if not force_no_spaces else ""
		indent = (space * indentation) if not force_no_indent else ""
		enter = "\n" if not force_no_indent else ""

		if trailing_commas is None:
			trailing_commas = 1

		if force_no_indent and trailing_commas < 2:
			trailing_commas = None

		load_dynamic_modules_if_needed()

		if is_mapping or (PydanticBM is not None and (able_simple(isinstance, it, PydanticBM) and isinstance(it, PydanticBM))):
			asterisks = FMT_ASTERISK[syntax_highlighting] * 2
		elif is_iterable:
			asterisks = FMT_ASTERISK[syntax_highlighting] * 1
		else:
			asterisks = ""

		if int_formatter is None and isinstance(it, bytearray):
			int_formatter = tcrhex

		if force_no_indent < 0:
			force_no_indent += 1

		thisdict = {
			"indentation": indentation,
			"item_limit": item_limit,
			"syntax_highlighting": syntax_highlighting,
			"trailing_commas": trailing_commas,
			"int_formatter": int_formatter,
			"let_no_indent": let_no_indent,
			"force_no_indent": force_no_indent,
			"force_no_spaces": force_no_spaces,
			"force_complex_parenthesis": force_complex_parenthesis,
			"force_slice_parenthesis": force_slice_parenthesis,
			"force_union_parenthesis": force_union_parenthesis,
			"prefer_full_names": prefer_full_names,
			"depth_limit": depth_limit,
			"prefer_pydantic_better_dump": prefer_pydantic_better_dump,
			"str_repr": str_repr,
			"no_implicit_quoteless": kwargs.get("no_implicit_quoteless", False),
			"no_try": kwargs.get("no_try"),
			"FMTC": FMTC,
			"__depth": kwargs.get("__depth", 2) + 1,
			"__seen": {*kwargs.get("__seen", {}), id(it)},
		}
		if a := kwargs.get("let_no_indent_max_iterables"):
			thisdict["let_no_indent_max_iterables"] = a
		if a := kwargs.get("let_no_indent_max_non_iterables"):
			thisdict["let_no_indent_max_non_iterables"] = a

		this = partial(fmt_iterable, **thisdict)
		str_repr = partial(str_repr, no_implicit_quoteless=kwargs.get("no_implicit_quoteless"))

		if syntax_highlighting and hasattr(it, "__tcr_rainbow__") and it.__tcr_rainbow__:
			if isinstance(it.__tcr_rainbow__, str):
				return gay(it.__tcr_rainbow__)

			_tcr_rainbow_queue_name = getattr_queue(
				it,
				name,
				"__name__",
				"__class__.__name__",
				default="__unknown_object__",
			)
			return gay(_tcr_rainbow_queue_name)

		queue_name = getattr_queue(
			type(it),
			name,
			"__name__",
			"__class__.__name__",
			default=("<???>" if syntax_highlighting else "__unknown_object__"),
		)

		if hasattr(it, "__tcr_display__") and callable(it.__tcr_display__):
			try:
				return it.__tcr_display__(**thisdict, _ran_from_tcr_display=True)
			except NotImplementedError:
				pass
			except Exception as e:
				if kwargs.get("_raise_errors") or "--tcr-raise-errors" in sys.argv:
					raise
				return FMT_INTERNAL_EXCEPTION[syntax_highlighting] % f"{queue_name}, {extract_error(e, raw=True)[0]}"

		if hasattr(it, "__tcr_fmt__") and callable(it.__tcr_fmt__):
			try:
				tcr_formatted = it.__tcr_fmt__(**thisdict, fmt_iterable=this, it=it, _ran_from_tcr_display=True)

				if tcr_formatted is not None:
					return tcr_formatted
			except NotImplementedError:
				pass
			except Exception as e:
				if kwargs.get("_raise_errors") or "--tcr-raise-errors" in sys.argv:
					raise
				return FMT_INTERNAL_EXCEPTION[syntax_highlighting] % f"{queue_name}, {extract_error(e, raw=True)[0]}"

		if not syntax_highlighting and isinstance(it, type):
			return it.__name__

		if "_force_next_type" in kwargs and kwargs.get("_ran_from_tcr_display"):
			return FMT_CLASS[syntax_highlighting] % (
				(queue_name + ("(...)" if not syntax_highlighting and not kwargs.get("_i_am_class") else "") + (FMT_LETTERS.META if syntax_highlighting and kwargs.get("_i_am_class") else "")),
				asterisks + this(it, no_implicit_quoteless=True),
			)

		if isinstance(it, _OverflowClass):
			return f"{FMTC.SPECIAL}({FMTC.NUMBER}{it}{FMTC.SPECIAL} more item{'s' if it.amount != 1 else ''}...){FMTC._}" if syntax_highlighting else f"({it} more items...)"
		if isinstance(it, slice):
			if not syntax_highlighting:
				return f"slice({it.start!r}, {it.stop}, {it.step})"

			if it.step is None:
				slice_params = (it.start, it.stop)
			else:
				slice_params = (it.start, it.stop, it.step)

			text = f"{FMTC.DECIMAL}:".join((f"{FMTC.NUMBER}{x!r}" if x is not None else "") for x in slice_params)

			if force_slice_parenthesis:
				text = FMT_BRACKETS[tuple][syntax_highlighting] % text

			return text

		if isinstance(it, ....__class__):  # cursed syntax lol
			if not syntax_highlighting:
				return "..."
			return f"{FMTC.DECIMAL}..."
		if able_simple_result(issubclass, it, Enum):
			return FMT_CLASS[syntax_highlighting] % (
				it.__name__ + (FMT_LETTERS.META if syntax_highlighting else ""),
				((1 if _is_enum_auto(it) else 2) * FMT_ASTERISK[syntax_highlighting])
				+ this(
					list(it),
					_force_next_type=set,
					let_no_ident=False,
					_enums_next_hide_class=True,
				),
			)

		if repr(it) == "<class 'pydantic.main.BaseModel'>":  # Kurwa pierdole tego kurwa pydantica chujowego
			return (FMTC.TYPE if syntax_highlighting else "") + "BaseModel"
		if isinstance(it, type) and hasattr(it, "__pydantic_core_schema__"):
			it_name = it.__pydantic_core_schema__

			while "schema" in it_name:
				it_name = it_name["schema"]

			it_name = it_name.get("model_name", "<UnknownPydanticType>")
			return (FMTC.TYPE if syntax_highlighting else "") + it_name
		if _HikariEnum is not None and able_simple_result(issubclass, it, _HikariEnum):
			return FMT_CLASS[syntax_highlighting] % (
				it.__name__ + (FMT_LETTERS.META if syntax_highlighting else ""),
				((1 if _is_enum_auto(it) else 2) * FMT_ASTERISK[syntax_highlighting])
				+ this(
					list(it),
					_force_next_type=set,
					let_no_ident=False,
					_enums_next_hide_class=True,
				),
			)
		if isinstance(it, Enum) or (_HikariEnum is not None and isinstance(it, _HikariEnum)):
			if kwargs.get("_enums_next_hide_class"):
				if _is_enum_auto(it.__class__):
					return FMT_ENUM_VARIANT_AUTO_NO_CLASS[syntax_highlighting] % _fmt_enum_variant_name(it.name, syntax_highlighting)
				else:
					return FMT_ENUM_VARIANT_NO_CLASS[syntax_highlighting] % (
						_fmt_enum_variant_name(it.name, syntax_highlighting),
						this(
							it.value,
							force_no_indent=True,
							force_complex_parenthesis=True,
						),
					)
			else:
				if _is_enum_auto(it.__class__):
					return FMT_ENUM_VARIANT_AUTO[syntax_highlighting] % (
						it.__class__.__name__,
						_fmt_enum_variant_name(it.name, syntax_highlighting),
					)
				return FMT_ENUM_VARIANT[syntax_highlighting] % (
					it.__class__.__name__,
					_fmt_enum_variant_name(it.name, syntax_highlighting),
					this(it.value, force_no_indent=True, force_complex_parenthesis=True),
				)
		if PydanticBM is not None and able_simple_result(isinstance, it, PydanticBM):
			if prefer_pydantic_better_dump:
				dumped = _pydantic_hopefully_non_erroring_dumper(it)
			else:
				try:
					dumped = it.model_dump(warnings="none")
				except Exception:
					# Pydantic doesn't feel like supporting sets nicely so it just errors when dumping. This just falls back to the other method and adds an exclamation mark to mark that it has errored and successfully recovered.
					dumped = _pydantic_hopefully_non_erroring_dumper(it)

			if dumped:
				return FMT_CLASS[syntax_highlighting] % (
					it.__class__.__name__,
					asterisks + this(dumped, no_implicit_quoteless=True),
				)
			else:
				return FMT_CLASS[syntax_highlighting] % (it.__class__.__name__, "")
		if isinstance(it, dt.datetime | dt.date | dt.time):
			if not syntax_highlighting:
				return f"{it.__class__.__name__}.fromisoformat({it.isoformat()!r})"
			else:
				if isinstance(it, dt.datetime):
					format_str = "%H:%M:%S.%f%z %d-%m-%Y, %a"
				elif isinstance(it, dt.date):
					format_str = "%d-%m-%Y, %a"
				else:
					format_str = "%H:%M:%S.%f%z"

				main_color = FMTC.NUMBER

				secondary_color = FMTC.COMMA if _is_date_in_the_past(it) else FMTC.DECIMAL

				zeroes_color = FMTC.NUMBER_NO_BOLD

				s = f"<{it:{format_str}}>"  # strftime <3

				for find, replace in {
					".000000": f".{zeroes_color}000000{main_color}",
					"00:": f"{zeroes_color}00:{main_color}",
					":00": f"{zeroes_color}:00{main_color}",
					"00.": f"{zeroes_color}00.{main_color}",
					"+0000": f"+{zeroes_color}0000{main_color}",
				}.items():
					s = s.replace(find, replace)

				for x in ("-", ":", "<", ">", ",", ".", "+"):
					s = s.replace(x, f"{secondary_color}{x}{main_color}")

				return s
		if isinstance(it, pathlib.PurePath):
			if not syntax_highlighting:
				return repr(it)

			drive, parts = it.drive, list(it.parts)

			if it.is_absolute() or (parts and (parts[0] == "" or parts[0] == "\\")):
				parts.pop(0)

			if drive:
				drive = f"{FMTC.STRING}{drive}".replace(":", f"{FMTC.COLON}:{FMTC.DECIMAL}")

			s = f"{FMTC.PATH_SLASH}/".join(([drive] if it.is_absolute() else ([""] if (it.parts and it.parts[0] == "\\") else [])) + [f"{FMTC.STRING}{part}" for part in parts])

			if "/" not in s:
				return FMT_CLASS[True] % (it.__class__.__name__, s)

			return s

		if able_simple_result(issubclass, it, BaseException):
			exc_name = extract_error(it, raw=True)[0]

			if not syntax_highlighting:
				return exc_name

			return f"{FMTC.BUILT_IN_EXCEPTION}{exc_name}"

		if not syntax_highlighting and isinstance(it, QuotelessString):
			return str(it)
		if not syntax_highlighting and isinstance(it, GayString):
			return str(it)
		if not syntax_highlighting and isinstance(it, BrainfuckCode):
			return str(it)

		if it is None:
			return f"{FMTC.NONE}{it}{FMTC._}" if syntax_highlighting else str(it)
		if it is True:
			return f"{FMTC.TRUE}{it}{FMTC._}" if syntax_highlighting else str(it)
		if it is False:
			return f"{FMTC.FALSE}{it}{FMTC._}" if syntax_highlighting else str(it)

		_t = kwargs.get("_force_next_type") or type(it)

		if _t is QuotelessString:
			return str_repr(it, quoteless=True, syntax_highlighting=syntax_highlighting)
		if _t is GayString:
			return gay(it)
		if _t is BrainfuckCode:
			return _fmt_brainfuck(it)

		if _t is type:
			return f"{FMTC.TYPE}{getattr_queue(it, '__name__', '__class__.__name__', default=it)}{FMTC._}" if syntax_highlighting else str(it)

		try:
			if not kwargs.get("_force_next_type"):
				itsmro = getattr_queue(it, "__mro__", "__class__.__mro__", default=())
				# It's-a me mro

				if str in itsmro:
					_t = str  # Things displayed as ['a', 'b', 'c', 'd'] if they inherited from str
				elif bytes in itsmro:
					_t = bytes
				else:
					for item in itsmro:
						if item in FMT_BRACKETS:
							_t = item
							break
		except TypeError:
			pass

		if it.__class__ == sys.version_info.__class__ and syntax_highlighting:
			fmtc = FMTC()
			fmtc.NUMBER = FMTC.DECIMAL
			return FMT_SYS_VERSION_INFO % this(it[:3], FMTC=fmtc)
		if _t is int:
			if int_formatter:
				it = int_formatter(it)
			return f"{FMTC.NUMBER}{it}{FMTC._}" if syntax_highlighting else str(it)
		if _t is float:
			return f"{FMTC.NUMBER}{str(it).replace('.', f'{FMTC.DECIMAL}.{FMTC.NUMBER}')}{FMTC._}" if syntax_highlighting else str(it)
		if _t is str:
			return str_repr(it, syntax_highlighting=syntax_highlighting)
		if _t is bytes:
			reprit = repr(it)
			return f"{FMTC.BYTESTR_B}{reprit[0]}{FMTC.QUOTES}{reprit[1]}{FMTC.STRING}{reprit[2:-1]}{FMTC.QUOTES}{reprit[-1]}{FMTC._}" if syntax_highlighting else repr(it)
		if _t is complex:
			brackets = ("", "") if (not force_complex_parenthesis) else (f"{FMTC.BRACKET}(", f"{FMTC.BRACKET})")
			return (
				f"""{brackets[0]}{FMTC.NUMBER}{int(it.real) if int(it.real) == it.real else str(it.real).replace(".", f"{FMTC.DECIMAL}.{FMTC.NUMBER}")}{FMTC._}{space}{FMTC.COMPLEX}+{space}{FMTC.NUMBER}{int(it.imag) if int(it.imag) == it.imag else str(it.imag).replace(".", f"{FMTC.DECIMAL}.{FMTC.NUMBER}")}{FMTC.COMPLEX}j{brackets[1]}{FMTC._}"""
				if syntax_highlighting
				else repr(it)
			)
		if _t is UnionType:
			if force_union_parenthesis:
				return FMT_BRACKETS[tuple][syntax_highlighting] % (FMT_UNION_SEPARATOR[syntax_highlighting].join(this(x) for x in unpack_union(it)))
			else:
				return FMT_UNION_SEPARATOR[syntax_highlighting].join(this(x) for x in unpack_union(it))

		if _t is bytes_iterator:
			return FMT_ITER[syntax_highlighting] % this(bytes(it))
		if _t is type(iter("a")) or _t is type(iter("\u1234")):  # str_ascii_iterator and str_iterator ????
			return FMT_ITER[syntax_highlighting] % this("".join(it), no_implicit_quoteless=True)
		if _t is bytearray_iterator:
			return FMT_ITER[syntax_highlighting] % this(bytearray(it))
		if _t is dict_keyiterator:
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=dict_keys, _ov=ov)
		if _t is dict_valueiterator:
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=dict_values, _ov=ov)
		if _t is dict_itemiterator:
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=dict_items, _ov=ov)
		if _t in (list_iterator, list_reverseiterator, zip_iterator):
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _ov=ov)
		if _t in (range_iterator, longrange_iterator):
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=range, _ov=ov)
		if _t is set_iterator:
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=set, _ov=ov)
		if _t is tuple_iterator:
			listit, ov = limited_iterable(it, item_limit)
			return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=tuple, _ov=ov)
		if _t is coroutine:
			return FMT_BRACKETS[coroutine][syntax_highlighting] % (getattr_queue(it, name, "__name__"))

		comma = f"{FMTC.COMMA}," if syntax_highlighting else ","

		is_of_prohibited_type = any(isinstance(it, x) for x in (typing._GenericAlias, typing._UnpackGenericAlias))
		# took me half an hour of debugging to discover that typing._GenericAlias contains an infinite amount of nested copies of typing._UnpackGenericAlias but only if you first iter then index not if you just index and it's a mess.

		if not is_of_prohibited_type and is_iterable:
			if kwargs.get("_enums_next_hide_class"):
				thisdict["_enums_next_hide_class"] = True
				this = partial(this, _enums_next_hide_class=True)

			itl, overflow = limited_iterable(it, item_limit)
			if not able_simple(len, it) or len(it) > 0:
				if is_mapping:
					if it is sys.modules:
						it = it.copy()  # Fix crash because changed size during iteration because reasons
					inner = f"{comma}{enter or space}".join([
						indent + (f"{k}{FMTC.COLON}:{FMTC._}{space}{v}" if syntax_highlighting else f"{k}:{space}{v}").replace(enter, f"{enter}{indent}")
						for k, v in {this(key): this(value) for key, value in it.items()}.items()
					]) + (comma if trailing_commas else "")

					return (FMT_BRACKETS[_t] if _t in FMT_BRACKETS else FMT_BRACKETS[dict])[syntax_highlighting] % f'{enter}{inner}{enter}'  # fmt: skip
				else:
					inner = f"{comma}{enter or space}".join([
						indent + x.replace("\n", f"\n{indent}")
						for x in [this(element) for element in itl]
						+ ([] if not (overflow if not kwargs.get("_ov") else kwargs.get("_ov")) else [this(_OverflowClass(overflow if not kwargs.get("_ov") else kwargs.get("_ov")))])
					]) + (comma if (trailing_commas or ((not kwargs.get("_force_tuple_no_trailing_comma_on_single_element")) and _t is tuple and len(it) == 1)) else "")

					return (FMT_BRACKETS[_t] if _t in FMT_BRACKETS else FMT_BRACKETS[None])[syntax_highlighting] % f'{enter}{inner}{enter}'  # fmt: skip
			else:
				if _t is set and not syntax_highlighting:
					return "set()"
				return (FMT_BRACKETS[_t] if _t in FMT_BRACKETS else FMT_BRACKETS[None])[syntax_highlighting] % (comma if _t is set else '')  # fmt: skip

		if not syntax_highlighting:
			return repr(it)

		try:
			parse_repr_name, parse_repr_args, parse_repr_kwargs = parse_repr_literal(repr(it))

			if not parse_repr_args and not parse_repr_kwargs:
				return FMT_UNKNOWN_NO_PARENS[syntax_highlighting] % (
					parse_repr_name,
					FMT_BRACKETS[tuple][syntax_highlighting] % "",
				)
			elif parse_repr_args and not parse_repr_kwargs:
				return FMT_UNKNOWN_NO_PARENS[syntax_highlighting] % (
					parse_repr_name,
					this(
						parse_repr_args,
						_force_tuple_no_trailing_comma_on_single_element=True,
						no_implicit_quoteless=True,
					),
				)
			elif not parse_repr_args and parse_repr_kwargs:
				return FMT_UNKNOWN_NO_PARENS[syntax_highlighting] % (
					parse_repr_name,
					FMT_BRACKETS[tuple][syntax_highlighting] % ((FMT_ASTERISK[syntax_highlighting] * 2) + this(parse_repr_kwargs, no_implicit_quoteless=True)),
				)
			else:
				return FMT_UNKNOWN_NO_PARENS[syntax_highlighting] % (
					parse_repr_name,
					FMT_BRACKETS[tuple][syntax_highlighting]
					% (
						FMT_ASTERISK[syntax_highlighting]
						+ this(parse_repr_args, no_implicit_quoteless=True)
						+ comma
						+ space
						+ (FMT_ASTERISK[syntax_highlighting] * 2)
						+ this(parse_repr_kwargs, no_implicit_quoteless=True)
					),
				)

			# If the repr looks like a instantiation Name(args, kw=args), etc. then parse it into a str(*tuple, **dict) nice looking, indentend thing.
		except (
			ValueError,
			TypeError,
		):  # parse repr failed or __repr__ returned a non-str value
			return _fmt_unknown_highlighted(it, queue_name, this=this)
			# If no hardcoded patterns match, return a str-repred version of whatever it is

	if not sys.gettrace():  # If debugger is not running, dont optimize since it is a hassle to get into the fmt_iterable func
		globals()["fmt_iterable"] = _reset_return_wrapper(fmt_iterable)
	# Done this way to trick the IDE code snippets since the deco forwards the *args, **kwargs to the decorated func anyway...
	# If i were to @decorate the def fmt_iterable it'd replace the code snippets with the decorated function's code snippets.
	# Or i'm a dumbass and there's a better way of doing it.. (<- probably this)

	def print_iterable(
		it: Iterable,
		*its: Iterable,
		raw: bool | None = None,
		recursive: bool | None = None,
		printhook: Callable[[str], None] = print,
		**kwargs,
	) -> None:
		"""### Print iterable as formatted string with optional syntax highlighting with the given printhook.

		This also supports primitive types to be included in the iterables although passing primitive types themselves is fine.

		For formatting the iterable (and having the result returned as str) use tcr.fmt_iterable().\\
		For debugging use tcr.console().

		Example:
		```py
		>>> print_iterable([10, 20, 30]) # Returns None, if you need str use fmt_iterable()
		[
		10,
		20,
		30,
		]
		>>> print_iterable({10: 20, 30: 40})
		{
		10: 20,
		30: 40,
		}
		```

		Args:
			it: Iterable, The iterable to format
			*its: Iterable, The same as above, if provided, it = (it, *its), can be omitted.
			indentation: int, How many spaces between where the list bracket is placed and the list items.
			item_limit: int, How many items in a list can be displayed before it's cut off. Any values < 1 will be set back to 1
			syntax_highlighting: bool, Whether or not terminal color codes should be added to make the code/iterables perttier. This also slightly changes the syntax. For example `'{,}'` with syntax highlighting and `'set()'` without. If you wish to copy & paste the iterable from terminal back to code set this to False although it may work with it set to true as well. The extra syntax safety does not support generators and `"(X more items...)"` messages that come from `item_limit`.
			trailing_commas: bool, whether or not to add trailing commas to lists (`'[\\n  10,\\n  20,\\n]'` vs `'[\\n  10,\\n  20\\n]'`). Psst: this can be set to 2 to force trailing commas although it's not recommended to use this as a feature.
			int_formatter: Callable[[int], str], A function that formats integers to a string. For example tcr.hex will format all integers as hex values. The tcr.hex formatter is automatically used unless other one was supplied
			let_no_indent: bool, Let the function automatically determine good spots to remove excessive enter-indent-syntax (for example "[\\n  10,\\n  20\\n]" - The list has only two, non iterable items or when the list has only one iterable or non iterable item)
			force_no_indent: bool, Force the condition above (let_no_spaces), skip any conditions listed there, never add extra enters or indents even if it may make the result unreadable. This effectively makes `indent` or `let_no_indent` irrelevant. This also sets `trailing_commas` to False.
			force_no_spaces: bool, Force remove any extra spaces (not including the objects' values for example strings will still be displayed with spaces). It removes spaces for example after commas, colons, etc. This effectively enables `force_no_indent` thus making `indent` or `let_no_indent` irrelevant.
			force_complex_parenthesis: bool, Force parenthesis when displaying `complex` type for example `(3 + 1j)` instead of `3+1j`. This has no effect when syntax highlighting is turned off.
			force_slice_parenthesis: bool, Force parenthesis when displaying `slice` type for example `(::-1)` instead of `::-1`. This has no effect when syntax highlighting is turned off.
			force_union_parenthesis: bool, Force parenthesis when displaying `union` type.` This has no effect when syntax highlighting is turned off.
			prefer_full_names: bool, whether or not to use the full names of objects if possible.
			let_no_indent_max_iterables: int = 1, (advanced) override the limit for iterables for the let_no_indent feature
			let_no_indent_max_non_iterables: int = 4, (advanced) override the limit for non-iterables for the let_no_indent feature
			str_repr: Callable[[str], str] = json_dumps, (advanced) override the default string repr callable
			prefer_pydantic_better_dump: bool = False, Will use the pydantic's custom dumper which prints the model name in more places, instead of leaving it only for the moment when pydantic SHITS ITS PANTS (raises random shitass errors). i have nothing more to say about this.

		If no formatting is set for an object, it can be defined using the __tcr_display__(self, **kwargs) or __tcr_fmt__(self, *, fmt_iterable, **kwargs) methods.
		"""
		result = fmt_iterable(it, *its, **kwargs)
		if recursive is not None:
			warn(
				"`recursive` is deprecated. It's always set to True in new print_iterable()",
				DeprecationWarning,
				stacklevel=2,
			)
		if raw:
			warn(
				"`raw` is deprecated. Use fmt_iterable() instead",
				DeprecationWarning,
				stacklevel=2,
			)
			return result
		printhook(result)


if True:  # fmt_ and Fmt

	def tcrfmt_dataclass_by_name_args_kwargs(
		*,
		fmt_iterable: Callable[..., str],
		syntax_highlighting: bool,
		name: str,
		obj_args: tuple[Any, ...] = (),
		obj_kwargs: dict[str, Any] = {},
	):
		if obj_args and obj_kwargs:
			body = (
				FMT_ASTERISK[syntax_highlighting]
				+ fmt_iterable(obj_args, syntax_highlighting=syntax_highlighting, _force_next_type=tuple)
				+ (FMTC.COMMA if syntax_highlighting else "")
				+ ", "
				+ FMT_ASTERISK[syntax_highlighting] * 2
				+ fmt_iterable(obj_kwargs, syntax_highlighting=syntax_highlighting, no_implicit_quoteless=True, _force_next_type=dict)
			)
		elif obj_args and not obj_kwargs:
			body = FMT_ASTERISK[syntax_highlighting] + fmt_iterable(obj_args, syntax_highlighting=syntax_highlighting, _force_next_type=tuple)
		elif not obj_args and obj_kwargs:
			body = FMT_ASTERISK[syntax_highlighting] * 2 + fmt_iterable(obj_kwargs, no_implicit_quoteless=True, syntax_highlighting=syntax_highlighting, _force_next_type=dict)
		elif not obj_args and not obj_kwargs:
			body = ""

		return FMT_CLASS[syntax_highlighting] % (name, body)

	class TcrFmt_KwargsDataclass:
		def __tcr_fmt__(self=None, *, fmt_iterable=None, syntax_highlighting, **kwargs):
			if self is None:
				raise NotImplementedError

			obj_kwargs = clean_dunder_dict(self.__dict__, strategy=2)

			return tcrfmt_dataclass_by_name_args_kwargs(
				fmt_iterable=fmt_iterable,
				syntax_highlighting=syntax_highlighting,
				name=self.__class__.__name__,
				obj_kwargs=obj_kwargs,
			)


if True:  # Misc

	def alert(s: str, *, printhook: Callable[[str], None] = print, raw=False) -> None:
		text = "".join([f"{(Fore.BLACK + Back.RED + Style.bold) if i % 2 == 0 else Fore.BLACK + Back.YELLOW}{x}" for i, x in enumerate(s)]) + Style.reset

		if raw:
			return text

		printhook(text)

	def gay(text: str, offset: int = 0) -> str:
		"""Turn a string gay. Happy pride :3"""  # noqa: D400
		colors = [
			Fore.LIGHT_RED,
			Fore.ORANGE_1,
			Fore.LIGHT_YELLOW,
			Fore.LIGHT_GREEN,
			Fore.LIGHT_MAGENTA,
			Fore.LIGHT_BLUE,
			Fore.purple_1b,
			Fore.purple_4b,
		]

		if text != "tcrutils":
			colors.pop()

		colors = colors + colors[1:-1:-1]

		result = ""

		for i, char in enumerate(text):
			color = colors[(i - offset) % len(colors)]
			result += color + Style.bold + char

		result += FMTC._
		return result
