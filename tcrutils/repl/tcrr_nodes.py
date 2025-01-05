import abc
import re
from typing import Generic, TypeVar

import colored

from ..src.tcr_print import FMTC

T = TypeVar("T")


class Node(Generic[T]):
	name: str
	children: tuple["Node | str", ...]

	text: str | None

	def __str__(self):
		return self.text

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		if self.text is not None:
			body = fmt_iterable(()).replace(")", "") + fmt_iterable(self.text) + fmt_iterable(()).replace("(", "")
		else:
			at = f"{FMTC.DECIMAL}@" if syntax_highlighting else "@"
			body = at + fmt_iterable(self.name) + fmt_iterable(self.children, _force_next_type=tuple, _force_tuple_no_trailing_comma_on_single_element=True)

		return f"{FMTC.TYPE}{self.__class__.__name__}{body}"

	def __init__(self, name: str, *children: "Node"):
		if self.__class__ is Node:
			raise RuntimeError("Cannot instantiate Node without subclassing.")

		self.name = name
		self.children = children
		self.text = None

	@abc.abstractmethod
	def match(self, s: str) -> tuple[str, str] | None:
		raise NotImplementedError("Must implement method match() for Node")

	def submit(self, s: str) -> None:
		self.text = s

	def display(self) -> str:
		if self.text is None:
			raise RuntimeError("Node cannot be displayed before it gets submitted via matching.")

		return f"{self.text}"


class DisposableNode(Generic[T], Node[T]):
	"""Marked to be skipped when using the data, but not when displaying, for example you dont care about the mandatory space between keywords and identifiers but you still want to display it to the user."""


class ConvertableNode(Generic[T], Node[T]):
	"""Marked to be converted into another node with the convert method, after being displayed, before being returned to data processing."""

	@abc.abstractmethod
	def convert(self) -> Node[T]:
		raise NotImplementedError("Must implement method convert for ConvertableNode")


class KeywordNode(Node[str]):
	matching_text_escaped: str

	def __init__(self, name: str, *children: Node):
		super().__init__(name, *children)
		self.matching_text_escaped = re.escape(name)

	def match(self, s: str) -> tuple[str, str] | None:
		m = re.match(rf"^({self.matching_text_escaped})((?:\s|$).*)$", s)

		if m is not None:
			return m.groups()
		return m

	def display(self):
		return f"{FMTC.COLON}{super().display()}{FMTC._}"


class AliasKeywordNode(KeywordNode, ConvertableNode):
	alias_to: str

	def __init__(self, alias_ARROW_name: str, *children: Node):
		if not isinstance(alias_ARROW_name, str) or alias_ARROW_name.count("->") != 1:
			raise RuntimeError('In AliasKeywordNode declaration the first parameter must be a str containing exactly one occurence of "->". like this: "alias_name->actual_name"')

		alias_to, name = alias_ARROW_name.split("->")

		alias_to = alias_to.strip()
		name = name.strip()

		super().__init__(name, *children)
		self.matching_text_escaped = re.escape(alias_to)
		self.alias_to = alias_to

	def convert(self) -> KeywordNode:
		node = KeywordNode(self.name, self.children)
		node.submit(self.text)
		return node


class UnknownNode(Node[str]):
	children: tuple[()]  # Cannot have children nodes

	def __init__(self, *, unknown_text: str):
		super().__init__(unknown_text)
		self.submit(unknown_text)
		self.children = ()

	def match(self, s) -> tuple[str, str]:
		m = re.match(r"^(.*)()$", s)

		if m is not None:
			return m.groups()
		return m

	def display(self):
		return f"{colored.Style.UNDERLINE + colored.Fore.RED}{super().display()}{FMTC._}"


class _RegexNodeBase(Generic[T], Node[T]):
	pattern: str

	def __init_subclass__(cls, pattern):
		cls.pattern = pattern
		return super().__init_subclass__()

	def match(self, s):
		m = re.match(self.pattern, s)

		if m is not None:
			return m.groups()
		return m


class EllipsisNode(_RegexNodeBase[Ellipsis], pattern=r"^(\.\.\.)(.*)$"):
	def display(self):
		return f"{FMTC.DECIMAL}{super().display()}{FMTC._}"


class SignedIntNode(_RegexNodeBase[int], pattern=r"^(-?\d+)(.*)$"):
	def display(self):
		return f"{FMTC.NUMBER}{super().display()}{FMTC._}"


class SignedFloatNode(_RegexNodeBase[float], pattern=r"^(-?(?:\d+\.?\d*|\.?\d+))(.*)$"):
	def display(self):
		return f"{FMTC.NUMBER}{super().display()}{FMTC._}"


class PyIdentifierNode(_RegexNodeBase[str], pattern=r"^([a-zA-Z_][a-zA-Z0-9_]*)(.*)$"):
	def display(self):
		return f"{FMTC.SLASH}{super().display()}{FMTC._}"


class PwshVariableNode(_RegexNodeBase[str], pattern=r"^(\$[a-zA-Z_][a-zA-Z0-9_]*|\$\{[^{}\s]+\})(.*)$"):
	def display(self):
		return f"{colored.Fore.GREEN + colored.Style.BOLD}{super().display()}{FMTC._}"


class DoublequoteStrNode(_RegexNodeBase[str], pattern=r'^"((?:[^"\\]|\\.)*)"(.*)$'):
	def display(self):
		return f'{FMTC.QUOTES}"{FMTC.STRING}{super().display()}{FMTC.QUOTES}"{FMTC._}'


class SinglequoteStrNode(_RegexNodeBase[str], pattern=r"^'((?:[^'\\]|\\.)*)'(.*)$"):
	def display(self):
		return f"{FMTC.QUOTES}'{FMTC.STRING}{super().display()}{FMTC.QUOTES}'{FMTC._}"


class WordBreakNode(DisposableNode, _RegexNodeBase[str], pattern=r"(\s|$)(.*)$"): ...


# class RobostrSeparatorNode(_RegexNodeBase, pattern=r"(!)(.*)$"): ...
