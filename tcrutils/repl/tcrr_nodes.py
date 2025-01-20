import abc
import re
from typing import Generic, TypeVar

import colored

from ..src.tcr_console import console as c
from ..src.tcr_print import FMTC, fmt_iterable
from .tcrr_parser import parse_and_submit_nodes


class UnaccountedForNodesError(RuntimeError):
	nodes: tuple["Node"]

	def __init__(self, *nodes: "Node", syntax_highlighting: bool = True):
		self.nodes = nodes
		super().__init__(fmt_iterable(nodes, syntax_highlighting=syntax_highlighting))


### Root class


class Node:
	__match_args__ = ("name", "text")

	name: str
	text: str | None

	children: list["Node | str"]
	children_optional: bool

	def __str__(self):
		return self.text

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		if self.text is not None:
			body = fmt_iterable(()).replace(")", "") + fmt_iterable(self.text if not isinstance(self, ParsableNode) else self.parse()) + fmt_iterable(()).replace("(", "")
		else:
			at = f"{FMTC.DECIMAL}@" if syntax_highlighting else "@"
			body = (
				at
				+ fmt_iterable(self.name)
				+ fmt_iterable(
					self.children,
					let_no_indent=all(isinstance(x, str) for x in self.children),
					_force_next_type=tuple if self.children_optional else list,
					_force_tuple_no_trailing_comma_on_single_element=True,
				)
			)

		return f"{FMTC.TYPE}{self.__class__.__name__}{body}"

	def __init__(self, name: str, *children: "Node", children_optional: bool = False):
		if self.__class__ is Node:
			raise RuntimeError("Cannot instantiate Node without subclassing.")

		self.name = name
		self.children = list(children)
		self.children_optional = children_optional
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


### Bases

T = TypeVar("T")


class ParsableNode(Node, Generic[T]):
	__match_args__ = ("name", "value")

	def _init__(self, *args, **kwargs):
		if self.__class__ is ParsableNode:
			raise RuntimeError("Cannot instantiate Node without subclassing.")

		super().__init__(*args, **kwargs)

	exec("__init__ = _init__; del _init__")

	@abc.abstractmethod
	def parse(self) -> T:
		raise NotImplementedError("Must implement method parse() for ParsableNode")

	@property
	def value(self) -> T:
		return self.parse()


class DisposableNode(Node):
	"""Marked to be skipped when using the data, but not when displaying, for example you dont care about the mandatory space between keywords and identifiers but you still want to display it to the user."""


class ConvertableNode(Node):
	"""Marked to be converted into another node with the convert method, after being displayed, before being returned to data processing."""

	@abc.abstractmethod
	def convert(self) -> Node:
		raise NotImplementedError("Must implement method convert for ConvertableNode")


class ExecutableNode(Node):
	"""An action is associated with this node, for example QuitNode: its action is to call exit(0)."""

	@abc.abstractmethod
	def execute(self) -> None:
		raise NotImplementedError("Must implement method execute for ExecutableNode")


class _RegexNodeBase(Node):
	pattern: str

	def __init_subclass__(cls, pattern):
		cls.pattern = pattern
		return super().__init_subclass__()

	def match(self, s):
		m = re.match(self.pattern, s)

		if m is not None:
			return m.groups()
		return m


### Usable nodes


class QuitNode(_RegexNodeBase, ExecutableNode, pattern=r"^(quit|q|exit)(.*)$"):
	def display(self):
		return f"{FMTC.GD_COLON}{super().display()}{FMTC._}"

	def execute(self):
		exit(0)


class UnreachableNode(Node):
	def match(self, s):
		return None


class IrrefutableNode(DisposableNode, Node):
	def match(self, s):
		return ("", s)

	def __init__(self, name: str = "_", *children: Node, **kwargs):
		super().__init__(name, *children, **kwargs)


class KeywordNode(Node):
	matching_text_escaped: str

	def __init__(self, name: str, *children: Node, children_optional: bool = False):
		super().__init__(name, *children, children_optional=children_optional)
		self.matching_text_escaped = re.escape(name)

	def match(self, s: str) -> tuple[str, str] | None:
		m = re.match(rf"^({self.matching_text_escaped})((?:\s|$).*)$", s)

		if m is not None:
			return m.groups()
		return m

	def display(self):
		return f"{FMTC.GD_COLON}{super().display()}{FMTC._}"


class AliasKeywordNode(KeywordNode, ConvertableNode):
	alias_to: str

	def __init__(self, alias_ARROW_name: str, *children: Node, children_optional: bool = False):
		if not isinstance(alias_ARROW_name, str) or alias_ARROW_name.count("->") != 1:
			raise RuntimeError('In AliasKeywordNode declaration the first parameter must be a str containing exactly one occurence of "->". like this: "alias_name->actual_name"')

		alias_to, name = alias_ARROW_name.split("->")

		alias_to = alias_to.strip()
		name = name.strip()

		super().__init__(name, *children, children_optional=children_optional)
		self.matching_text_escaped = re.escape(alias_to)
		self.alias_to = alias_to

	def convert(self) -> KeywordNode:
		node = KeywordNode(self.name, *self.children, children_optional=self.children_optional)
		node.submit(self.text)
		return node


class UnknownNode(Node):
	children: list  # Cannot have children nodes

	def __init__(self, *, unknown_text: str):
		super().__init__(unknown_text)
		self.submit(unknown_text)
		self.children = []

	def match(self, s) -> tuple[str, str]:
		m = re.match(r"^(.*)()$", s)

		if m is not None:
			return m.groups()
		return m

	def display(self):
		return f"{colored.Style.UNDERLINE + colored.Fore.RED}{super().display()}{FMTC._}"


class IncompleteNode(UnknownNode): ...


class EllipsisNode(_RegexNodeBase, ParsableNode[Ellipsis], pattern=r"^(\.\.\.)(.*)$"):
	def display(self):
		return f"{FMTC.DECIMAL}{super().display()}{FMTC._}"

	def parse(self):
		return ...


class IntNode(_RegexNodeBase, ParsableNode[int], pattern=r"^(-?\d+)(.*)$"):
	def display(self):
		return f"{FMTC.NUMBER}{super().display()}{FMTC._}"

	def parse(self) -> T:
		return int(self.text)


class SignedFloatNode(_RegexNodeBase, pattern=r"^(-?(?:\d+\.?\d*|\.?\d+))(.*)$"):
	def display(self):
		return f"{FMTC.NUMBER}{super().display()}{FMTC._}"


class PyIdentifierNode(_RegexNodeBase, pattern=r"^([a-zA-Z_][a-zA-Z0-9_]*)(.*)$"):
	def display(self):
		return f"{FMTC.DECIMAL}{super().display()}{FMTC._}"


class PwshVariableNode(_RegexNodeBase, pattern=r"^(\$[a-zA-Z_][a-zA-Z0-9_]*|\$\{[^{}\s]+\})(.*)$"):
	def display(self):
		return f"{colored.Fore.GREEN + colored.Style.BOLD}{super().display()}{FMTC._}"


class DoublequoteStrNode(_RegexNodeBase, pattern=r'^"((?:[^"\\]|\\.)*)"(.*)$'):
	def display(self):
		return f'{FMTC.QUOTES}"{FMTC.STRING}{super().display()}{FMTC.QUOTES}"{FMTC._}'


class SinglequoteStrNode(_RegexNodeBase, pattern=r"^'((?:[^'\\]|\\.)*)'(.*)$"):
	def display(self):
		return f"{FMTC.QUOTES}'{FMTC.STRING}{super().display()}{FMTC.QUOTES}'{FMTC._}"


class WordBreakNode(DisposableNode, _RegexNodeBase, pattern=r"^(\s|$)(.*)$"): ...


class _CompoundNodeMatchedMarkerNode(IrrefutableNode, DisposableNode): ...


class CompoundNode(Node):
	_parsed: None | tuple[Node]
	nodes: tuple[Node]
	require_matched_marker: bool

	def _init__(self, *args, **kwargs):
		if self.__class__ is CompoundNode:
			raise RuntimeError("Cannot instantiate CompoundNode without subclassing.")

		self._parsed = None

		super().__init__(*args, **kwargs)

	exec("__init__ = _init__; del _init__")

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		if self.text is None:
			at = f"{FMTC.DECIMAL}@" if syntax_highlighting else "@"
			body = (
				fmt_iterable(self.nodes, _force_next_type=list)
				+ at
				+ fmt_iterable(self.name)
				+ fmt_iterable(
					self.children,
					let_no_indent=all(isinstance(x, str) for x in self.children),
					_force_next_type=tuple if self.children_optional else list,
					_force_tuple_no_trailing_comma_on_single_element=True,
				)
			)
		elif isinstance(self, ParsableNode):
			body = fmt_iterable(()).replace(")", "") + fmt_iterable(self.parse()) + fmt_iterable(()).replace("(", "")
		else:
			body = fmt_iterable(self._parsed)

		return f"{FMTC.TYPE}{self.__class__.__name__}{body}"

	def __init_subclass__(cls, nodes, require_matched_marker=False, **kwargs):
		cls.nodes = nodes()
		cls.require_matched_marker = require_matched_marker

		super().__init_subclass__(**kwargs)

	def match(self, s):
		parsed = parse_and_submit_nodes(s, self.nodes)

		if self.require_matched_marker and not any(isinstance(x, _CompoundNodeMatchedMarkerNode) for x in parsed):
			return None

		match parsed[-1]:
			case UnknownNode():
				parsed = parsed[:-1]  # Accounted for with s.removeprefix(text), since text wouldnt contain the unknown node text.

		incomplete = bool(parsed and not parsed[-1].children_optional and parsed[-1].children)

		self._parsed = parsed

		text = "".join(x.text for x in parsed)

		if not text:
			return None

		return text, s.removeprefix(text), incomplete

	def display(self):
		return "".join(x.display() for x in self._parsed)


if True:  # String

	class _StringDQuoteNode(DisposableNode, _RegexNodeBase, pattern=r'^(")(.*)$'):
		def display(self):
			return f'{FMTC.QUOTES}"{FMTC._}'

	class _StringSQuoteNode(DisposableNode, _RegexNodeBase, pattern=r"^(')(.*)$"):
		def display(self):
			return f"{FMTC.QUOTES}'"

	class _StringDQContent(_RegexNodeBase, pattern=r'^((?:[^"\\]|\\.)*)(.*)$'):
		def display(self):
			return f"{FMTC.STRING}{super().display()}"

	class _StringSQContent(_RegexNodeBase, pattern=r"^((?:[^'\\]|\\.)*)(.*)$"):
		def display(self):
			return f"{FMTC.STRING}{super().display()}"

	class String(
		CompoundNode,
		ParsableNode[str],
		nodes=lambda: (
			UnreachableNode(
				"juncdq",
				_StringDQContent(
					"contentdq",
					_StringDQuoteNode("dqclose"),
				),
			),
			UnreachableNode(
				"juncsq",
				_StringSQContent(
					"contentsq",
					_StringSQuoteNode("sqclose"),
				),
			),
			_StringDQuoteNode(
				"dqopen",
				_CompoundNodeMatchedMarkerNode("_", "juncdq/*"),
			),
			_StringSQuoteNode(
				"sqopen",
				_CompoundNodeMatchedMarkerNode("_", "juncsq/*"),
			),
		),
	):
		def parse(self) -> str:
			parsed = [x for x in self._parsed if not isinstance(x, DisposableNode)]

			if len(parsed) != 1:
				raise RuntimeError("Malformed str parsing??? Expected only 1 Node left: _StringDQContent or _StringSQContent")

			return parsed[0].text.encode("utf-8").decode("unicode_escape")


if True:  # List

	class _ListOpeningBracketNode(DisposableNode, _RegexNodeBase, pattern=r"^(\[)(.*)$"): ...

	class _ListClosingBracketNode(DisposableNode, _RegexNodeBase, pattern=r"^(\])(.*)$"): ...

	class _ListCommaNode(DisposableNode, _RegexNodeBase, pattern=r"^(,)(.*)$"): ...

	class _GenericListNode(
		CompoundNode,
		ParsableNode[list[T]],
		Generic[T],
		require_matched_marker=True,
		nodes=lambda: (
			UnreachableNode(
				"junc",
				WordBreakNode(
					"wordbreak",
					"junc/*",
				),
				_ListCommaNode(
					",",
					"content/*",
				),
				_ListClosingBracketNode("]"),
			),
			IrrefutableNode(
				"",
				_CompoundNodeMatchedMarkerNode(
					"_",
					_ListOpeningBracketNode(
						"[",
						"content/*",
						WordBreakNode("wordbreak", "/_/[/*", "junc/]"),
						"junc/]",
					),
				),
			),
		),
	):
		def _init__(self, *args, **kwargs):
			if self.__class__ is _GenericListNode:
				raise RuntimeError("Cannot instantiate _GenericListNode without subclassing.")

			return super().__init__(*args, **kwargs)

		exec("__init__ = _init__; del _init__")

		def parse(self) -> list:
			parsed = [x for x in self._parsed if not isinstance(x, DisposableNode)]

			l = []

			for node in parsed:
				l.append(node.parse())

			return l

		def __init_subclass__(cls, listof):
			listof = [x(f"listitem{i}", "junc/*") for i, x in enumerate(listof)]

			content_unreachable_node = UnreachableNode(
				"content",
				*listof,
				WordBreakNode(
					"content-wordbreak",
					"content/*",
				),
				_ListClosingBracketNode("]"),
			)

			cls.nodes = (*cls.nodes, content_unreachable_node)

	class ListOfInt(_GenericListNode[int], listof=(IntNode,)): ...

	class ListOfStr(_GenericListNode[str], listof=(String,)): ...

	class ListOfStrOrInt(_GenericListNode[int | str], listof=(IntNode, String)): ...

# class RobostrSeparatorNode(_RegexNodeBase, pattern=r"(!)(.*)$"): ...
