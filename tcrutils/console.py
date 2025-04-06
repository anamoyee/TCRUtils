import datetime
import inspect
import re as regex
from collections.abc import Callable
from functools import partial, reduce
from sys import argv, exit

from colored import Back, Fore, Style

from .dict import clean_dunder_dict
from .extract_error import extract_error, extract_traceback
from .getch import getch
from .inspect import eval_fback, get_file_colon_lineno
from .iterable import cut_at
from .print import FMTC, fmt_iterable
from .terminal import terminal
from .types import QuotelessString


class CC:
	_ = Style.reset
	LOG = Fore.light_green + Style.bold  # 10
	WARN = Fore.YELLOW + Style.bold
	ERROR = Fore.RED + Style.bold
	DEBUG = Fore.purple_1b + Style.bold  # 129
	CRITICAL = Back.RED + Style.bold
	BANG = Fore.WHITE + Back.RED + Style.bold


class Console:
	"""### Provides logging capabilities.

	`console(...)` == `console.debug(...)`
	"""

	header_exprs: list[tuple[str, bool]]
	header_joiner: str
	header_end: str
	_last_diff: str | None = None
	include_callsite: bool = None

	def __init__(self, *, header_exprs: list[tuple[str, bool]] = None, header_joiner: str = ".", header_end: str = ": ") -> None:
		self.header_exprs = header_exprs or []
		self.header_joiner = header_joiner
		self.header_end = header_end

	@staticmethod
	def _get_timestamp():
		return str(datetime.datetime.now())[:-3].replace(".", ",")

	def _get_callsite_text_if_enabled(self, backtrack_frames) -> str:
		if self.include_callsite or (self.include_callsite is None and "--tcr-c-callsite" in argv):
			return get_file_colon_lineno(backtrack_frames=backtrack_frames)
		return ""

	def evaluate_header(self, fback_count: int = 5) -> str:
		result_list = [(expr if is_literal else eval_fback(expr, fback_count=fback_count)) for expr, is_literal in self.header_exprs]
		result_str = self.header_joiner.join(str(x) for x in result_list if x is not None)
		if result_str:
			result_str += self.header_end

		return result_str

	def _generate_out_and_print(self, *values, sep="\n", end="", withprefix=True, syntax_highlighting: bool = True, color: str, letter: str, _this_iteration_header: str | None = None, **kwargs) -> None:
		if _this_iteration_header is None:
			_this_iteration_header = self.evaluate_header()

		if not values:
			values = ("",)

		if len(values) > 1:
			for i, v in enumerate(values):
				if i == 0:
					char = "V"
				elif i == len(values) - 1:
					char = "Λ"
				else:
					char = "│"

				print(char, end=" ")

				self._generate_out_and_print(v, sep=sep, end=end, withprefix=withprefix, syntax_highlighting=syntax_highlighting, color=color, letter=letter, _this_iteration_header=_this_iteration_header, **kwargs)
			return

		values = [(f"{_this_iteration_header or ''}{x}" if isinstance(x, str) else fmt_iterable(x, syntax_highlighting=syntax_highlighting, **kwargs)) for x in values]

		out = sep.join(values)
		out = reduce(lambda x, y: str(x) + sep + str(y), [*values, ""])

		if withprefix:
			out = f"{letter} {(self._get_callsite_text_if_enabled(4) + ' ').lstrip()}{self._get_timestamp()} " + out

		out = f"{color if syntax_highlighting else ''}{out}{CC._ if syntax_highlighting else ''}"

		print(out, end=end)

	def log(self, *values, sep=" ", end="\n", withprefix=True) -> None | str:
		self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.LOG, letter="I")

	def warn(self, *values, sep=" ", end="\n", withprefix=True) -> None | str:
		self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.WARN, letter="W")

	def error(self, *values, sep=" ", end="\n", withprefix=True) -> None | str:
		self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.ERROR, letter="E")

	def critical(self, *values, sep=" ", end="\n", withprefix=True) -> None | str:
		self._generate_out_and_print(*values, sep=sep, end=end, withprefix=withprefix, color=CC.CRITICAL, letter="C")

	def debug(
		self,
		value: object = ...,
		/,
		*values: object,
		withprefix: bool = True,
		passthrough: bool = False,
		printhook: Callable[[str], None] = print,
		syntax_highlighting=True,
		margin: str = "",
		padding: str = " ",
		quoteless: bool = True,
		diff: bool = False,
		fmt_iterable: Callable[..., str] = fmt_iterable,
		eval: bool = False,
		**kwargs,
	) -> None | object:
		all_values = (value, *values)

		eval_header = self.evaluate_header(6)

		if eval_header:
			padding += eval_header

		if eval and len(all_values) == 1 and isinstance(all_values[0], str):
			pattern = regex.compile(r"^(.*?) ?(?:(?:=)|(?:->)|(?:=>)) ?$")
			match = pattern.match(all_values[0])

			if match:
				expression = match.group(1)

				result = eval_f_back(expression, f_backs=2)

				all_values = (all_values[0], result)
			else:
				raise ValueError("eval=True, but the only parameter's structure is invalid, must be a str that ends with '=', if you only want to pretty print, DO NOT USE THE eval=True KWARG!")
		elif eval:
			if len(all_values) != 1:
				raise ValueError("eval=True, but there is not exactly 1 positional parameter, if you only want to pretty print, DO NOT USE THE eval=True KWARG!")
			raise ValueError("eval=True, but the only parameter's structure is invalid, must be a str, if you only want to pretty print, DO NOT USE THE eval=True KWARG!")

		if len(all_values) >= 2 and all_values[0].__class__ is str and all_values[0]:
			first_string: str = all_values[0]
			after_first_string = ""

			found_any = False

			for symbol in ("=", "->", "=>"):
				if first_string.rstrip().endswith(symbol):
					found_any = True
					first_string = first_string.rstrip().removesuffix(symbol)
					if first_string and first_string[-1] == " ":
						after_first_string = f"{symbol} "
					else:
						after_first_string = symbol

			if found_any:
				if not withprefix and padding == " ":
					padding = ""
				padding += fmt_iterable(QuotelessString(first_string), syntax_highlighting=syntax_highlighting, **kwargs)
				padding += after_first_string

				quoteless = False
				all_values = all_values[1:]

		out = fmt_iterable(*[(x if ((not quoteless) or (x.__class__ is not str) or x == "" or x.strip() != x) else QuotelessString(x)) for x in all_values], syntax_highlighting=syntax_highlighting, **kwargs)

		if padding == " " and not withprefix:
			padding = ""

		prefix = ""
		if withprefix:
			prefix = f"D {(self._get_callsite_text_if_enabled(3) + ' ').lstrip()}{self._get_timestamp()}"

		c_debug = ""
		c_reset = ""
		c_bang = ""
		if syntax_highlighting:
			c_debug = CC.DEBUG
			c_reset = CC._
			c_bang = CC.BANG

		def compose(x) -> str:
			return f"{c_debug}{margin}{prefix}{padding}{x}{c_reset}"

		if diff and not self._last_diff:
			printhook(compose("\n" + "\n".join(["  " + x for x in out.split("\n")])))
		else:
			if not diff:
				printhook(compose(out))
			else:
				out_lines = out.split("\n")
				last_lines = self._last_diff.split("\n")

				while len(out_lines) < len(last_lines):
					last_lines.pop(-1)

				while len(last_lines) < len(out_lines):
					last_lines.append("")

				diff_out = "\n".join([("  " if line == line_old else f"{c_bang}*{c_reset} ") + line for line, line_old in zip(out_lines, last_lines, strict=True)])

				printhook(compose("\n" + diff_out))

		self._last_diff = out
		return None if not passthrough else value

	def hr(self, newlines_on_both_sides: bool = True, **kwargs):
		if newlines_on_both_sides:
			print()
		self.debug(QuotelessString("=" * terminal.width), withprefix=False, **kwargs)
		if newlines_on_both_sides:
			print()

	def with_expr_header(self, header_expr: str, literal: bool = False, joiner: str | None = None, end: str | None = None) -> "Console":
		if not isinstance(header_expr, str):
			raise TypeError("header_expr must be a string")

		if joiner is not None:
			if not isinstance(joiner, str):
				raise TypeError("overwrite_header_joiner must be a string")

		if end is not None:
			if not isinstance(end, str):
				raise TypeError("overwrite_header_end must be a string")

		return Console(
			header_exprs=self.header_exprs + [(header_expr, literal)],
			header_joiner=joiner if joiner is not None else self.header_joiner,
			header_end=end if end is not None else self.header_end,
		)

	def with_header(self, header: str):
		"""Add a simple header, alias for `with_expr_header(header, literal=True)`."""
		return self.with_expr_header(header, literal=True)

	__call__ = debug

	def __or__(self, other):
		return self.debug(other, passthrough=True)

	def __ror__(self, other):
		return self.debug(other, passthrough=True)

	def __repr__(self):
		return f"{self.__class__.__name__}()"

	def __lshift__(self, other):
		self.debug(other)
		return self

	def __rrshift__(self, other):
		self.debug(other)
		return self

	def __xor__(self, other):
		self.debug(other, withprefix=False)
		return other

	def __rxor__(self, other):
		self.debug(other, withprefix=False)
		return other


c = console = Console()
"""### Provides logging capabilities.

  `console(...)` == `console.debug(...)`
"""


def _clean_built_in_methods(d: dict) -> dict:
	return {k: v for k, v in d.items() if not isinstance(v, type(abs))}


def eval_f_back(code: str, *, f_backs: int = 1):
	"""Evaluates `code` in the context of the caller `f_backs` frames back."""

	frame = inspect.currentframe()
	for _ in range(f_backs):
		frame = frame.f_back

	return eval(code, frame.f_globals, frame.f_locals)


def start_eval_session(f_backs: int = 1) -> None:
	"""Starts an interactive shell. For debugging purposes."""
	try:
		current_frame = inspect.currentframe()
		for _ in range(f_backs):
			current_frame = current_frame.f_back
		desired_locals = current_frame.f_locals
		desired_globals = current_frame.f_globals

		a = " "
		while a:
			a = input("\n\r>>> ")
			if a:
				try:
					if a.strip().lower() == "locals":
						console(_clean_built_in_methods(clean_dunder_dict(desired_locals)))
					elif a.strip().lower() == "globals":
						console(_clean_built_in_methods(clean_dunder_dict(desired_globals)))
					elif a.strip().lower() == "code":
						lines, _ = inspect.findsource(current_frame)
						lineno = current_frame.f_lineno

						AROUND = 2
						CUTOFF = 70

						lines = lines[max(0, lineno - (AROUND + 1)) : lineno + AROUND]
						while all(x.startswith(" ") for x in lines):
							lines = [x[1:] for x in lines]
						lines = [f"{FMTC.NUMBER}{lineno - AROUND + i}{Fore.yellow + Style.bold} {'>' if i == AROUND else '|'}{FMTC._} {cut_at(x, CUTOFF)}" for i, x in enumerate(lines)]
						lines = "".join(lines)

						print(lines)
					else:
						console(eval(a, desired_locals, desired_globals))
				except Exception as e:
					console.error(f"\n\n{extract_traceback(e)}\n{extract_error(e)}")
	except (KeyboardInterrupt, EOFError):
		print("\r" + (" " * terminal.width) + "\r", end="")
		exit()


def breakpoint(*vals, printhook=console, clear=True, ctrlc: Callable[[], None] = start_eval_session) -> None:
	"""Stop the program execution until a key is pressed. Optionally pass in things to print."""
	vals and printhook(*vals)
	print(
		(a := f"{Fore.WHITE + Style.BOLD} >>> {Back.RED}BREAKPOINT{Style.RESET} {Fore.WHITE + Style.BOLD}<<<{Style.RESET}"),
		end="\r",
	)

	if getch() == b"\x03":
		if clear:
			print(len(a) * " ", end="")
		ctrlc()
		return

	if clear:
		print(len(a) * " ", end="\r")
	else:
		print()
