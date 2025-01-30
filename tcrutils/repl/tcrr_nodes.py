import abc
import datetime
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
					_force_tuple_no_trailing_comma_on_single_element=True,
				)
			)

		return f"{FMTC.TYPE}{self.__class__.__name__}{body}"

	def __init__(self, name: str = "", *children: "Node"):
		if self.__class__ is Node:
			raise RuntimeError("Cannot instantiate Node without subclassing.")

		self.name = name
		self.children = list(children)
		self.text = None

	@abc.abstractmethod
	def match(self, s: str) -> tuple[str, str] | None:
		raise NotImplementedError("Must implement method match() for Node")

	def submit(self, s: str) -> None:
		self.text = s


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


class OwnDisplayNode(Node):
	def display(self) -> str:
		return self.text


if True:  # Bases

	class _RegexNodeBase(Node):
		pattern: str

		def __init_subclass__(cls, *, pattern, **kw):
			cls.pattern = pattern
			super().__init_subclass__(**kw)

		def match(self, s):
			m = re.match(self.pattern, s)

			if m is not None:
				return m.groups()
			return m

	class _StartswithNodeBase(Node):
		startswith_texts: list[str]

		def __init_subclass__(cls, *, startswith: tuple[str] | str, **kw):
			cls.startswith_texts = sorted((startswith,) if isinstance(startswith, str) else startswith, key=len, reverse=True)
			super().__init_subclass__(**kw)

		def match(self, s):
			for startswith_text in self.startswith_texts:
				if s.startswith(startswith_text):
					return (s[: len(startswith_text)], s[len(startswith_text) :])

			return None


class LiteralNode(Node):
	def match(self, s):
		if not s.startswith(self.name):
			return None

		return s[: len(self.name)], s[len(self.name) :]


class DisposableLiteralNode(DisposableNode, LiteralNode): ...


class UnreachableNode(Node):
	def match(self, s):
		return None


class IrrefutableNode(DisposableNode, Node):
	def match(self, s):
		return ("", s)

	def __init__(self, name: str = "_", *children: Node, **kwargs):
		super().__init__(name, *children, **kwargs)


class KeywordNode(OwnDisplayNode):
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
		return f"{FMTC.GD_COLON}{super().display()}{FMTC._}"


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
		node = KeywordNode(self.name, *self.children)
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


class IncompleteNode(UnknownNode): ...


class EllipsisNode(OwnDisplayNode, _StartswithNodeBase, ParsableNode[Ellipsis], startswith="..."):
	def parse(self):
		return ...

	def display(self):
		return f"{FMTC.DECIMAL}{super().display()}{FMTC._}"


class IntNode(OwnDisplayNode, _RegexNodeBase, ParsableNode[int], pattern=r"^(-?\d+)(.*)$"):
	min: int | None = None
	max: int | None = None

	def __init_subclass__(cls, *, min: int = None, max: int = None):
		cls.min = min
		cls.max = max

	def match(self, s):
		result = super().match(s)
		if result is None:
			return None

		if self.min is None and self.max is None:
			return result

		parsed = int(result[0])

		if self.min is not None and self.min > parsed:
			return None

		if self.max is not None and self.max < parsed:
			return None

		return result

	def display(self):
		return f"{FMTC.NUMBER}{self.text}{FMTC._}"

	def parse(self) -> T:
		return int(self.text)


if True:  # Int-based Time & Date

	class Hour24IntNode(IntNode, min=0, max=23): ...

	class MinuteOrSecondIntNode(IntNode, min=0, max=59): ...

	class YearNode(IntNode, min=1000, max=9999): ...

	class MonthNode(IntNode, min=1, max=12): ...

	class DayNode(IntNode, min=1, max=31): ...


class FloatNode(OwnDisplayNode, _RegexNodeBase, ParsableNode[float], pattern=r"^(-?(?:\d+\.?\d*|\.?\d+))(.*)$"):
	def display(self):
		return f"{FMTC.NUMBER}{super().display()}{FMTC._}".replace(".", f"{FMTC.DECIMAL}.{FMTC.NUMBER}")

	def parse(self):
		return float(self.text)


class WordNode(OwnDisplayNode, _RegexNodeBase, pattern=r"^([a-zA-Z]+)(.*)$"): ...


class PyIdentifierNode(_RegexNodeBase, pattern=r"^([a-zA-Z_][a-zA-Z0-9_]*)(.*)$"):
	def display(self):
		return f"{FMTC.DECIMAL}{super().display()}{FMTC._}"


class DoublequoteStrNode(OwnDisplayNode, _RegexNodeBase, pattern=r'^"((?:[^"\\]|\\.)*)"(.*)$'):
	def display(self):
		return f'{FMTC.QUOTES}"{FMTC.STRING}{super().display()}{FMTC.QUOTES}"{FMTC._}'


class SinglequoteStrNode(OwnDisplayNode, _RegexNodeBase, pattern=r"^'((?:[^'\\]|\\.)*)'(.*)$"):
	def display(self):
		return f"{FMTC.QUOTES}'{FMTC.STRING}{super().display()}{FMTC.QUOTES}'{FMTC._}"


class WordBreakNode(DisposableNode, _RegexNodeBase, pattern=r"^(\s|$)(.*)$"): ...


class CompoundNodeMatchedMarkerNode(IrrefutableNode): ...


class CompoundNode(Node):
	_parsed: None | list[Node]
	nodes: list[Node]
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
					_force_tuple_no_trailing_comma_on_single_element=True,
				)
			)
		else:
			if isinstance(self, ParsableNode):
				try:
					parsed = self.parse()
				except Exception:
					parsed = "< FAILED TO PARSE >"
				body = fmt_iterable(()).replace(")", "") + fmt_iterable(parsed) + fmt_iterable(()).replace("(", "") + fmt_iterable([None] if self._parsed is None else [x for x in self._parsed if not isinstance(x, DisposableNode)])
			else:
				body = fmt_iterable(self._parsed)

		return f"{FMTC.TYPE}{self.__class__.__name__}{body}"

	def __init_subclass__(cls, nodes: list[Node], require_matched_marker: bool = False, **kwargs):
		cls.nodes = list(nodes)
		cls.require_matched_marker = require_matched_marker

		super().__init_subclass__(**kwargs)

	def match(self, s):
		parsed = parse_and_submit_nodes(s, self.nodes)

		if self.require_matched_marker and not any(isinstance(x, CompoundNodeMatchedMarkerNode) for x in parsed):
			return None

		match parsed[-1]:
			case UnknownNode():
				parsed = parsed[:-1]  # Accounted for with s.removeprefix(text), since text wouldnt contain the unknown node text.

		incomplete = bool(parsed and parsed[-1].children)

		self._parsed = list(parsed)

		text = "".join(x.text for x in parsed if not isinstance(x, IncompleteNode))

		if not text:
			return None

		return text, s.removeprefix(text), incomplete


if True:  # String

	class _StringDQuoteNode(DisposableNode, OwnDisplayNode, _RegexNodeBase, pattern=r'^(")(.*)$'): ...

	class _StringSQuoteNode(DisposableNode, OwnDisplayNode, _RegexNodeBase, pattern=r"^(')(.*)$"): ...

	class _StringDQContent(_RegexNodeBase, OwnDisplayNode, pattern=r'^((?:[^"\\]|\\.)*)(.*)$'): ...

	class _StringSQContent(_RegexNodeBase, OwnDisplayNode, pattern=r"^((?:[^'\\]|\\.)*)(.*)$"): ...

	class StringNode(
		OwnDisplayNode,
		CompoundNode,
		ParsableNode[str],
		nodes=(
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
				CompoundNodeMatchedMarkerNode("_", "juncdq/*"),
			),
			_StringSQuoteNode(
				"sqopen",
				CompoundNodeMatchedMarkerNode("_", "juncsq/*"),
			),
		),
	):
		def parse(self) -> str:
			parsed = [x for x in self._parsed if not isinstance(x, DisposableNode)]

			if len(parsed) != 1:
				raise RuntimeError("Malformed str parsing??? Expected only 1 Node left: _StringDQContent or _StringSQContent")

			return parsed[0].text.encode("utf-8").decode("unicode_escape")

		def display(self):
			s = ""
			for n in self._parsed:
				match n:
					case _StringDQuoteNode(text=text) | _StringSQuoteNode(text=text):
						s += f"{FMTC.QUOTES}{text}"
					case _StringDQContent(text=text) | _StringSQContent(text=text):
						s += f"{FMTC.STRING}{text}"
			return f"{s}{FMTC._}"


if True:  # List

	class _ListOpeningBracketNode(OwnDisplayNode, DisposableNode, _StartswithNodeBase, startswith="["):
		def display(self):
			return f"{FMTC.DECIMAL}{self.text}"

	class _ListClosingBracketNode(OwnDisplayNode, DisposableNode, _StartswithNodeBase, startswith="]"):
		def display(self):
			return f"{FMTC.DECIMAL}{self.text}{FMTC._}"

	class _ListCommaNode(OwnDisplayNode, DisposableNode, _StartswithNodeBase, startswith=","):
		def display(self):
			return f"{FMTC.DECIMAL}{self.text}{FMTC._}"

	class _GenericListNode(
		CompoundNode,
		ParsableNode[list[T]],
		Generic[T],
		require_matched_marker=True,
		nodes=(
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
				CompoundNodeMatchedMarkerNode(
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
		_symlink_to_content_node: UnreachableNode

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
			cls._symlink_to_content_node = content_unreachable_node

			cls.nodes.append(content_unreachable_node)

	class ListOfInt(_GenericListNode[int], listof=(IntNode,)): ...

	class ListOfStr(_GenericListNode[str], listof=(StringNode,)): ...

	class ListOfStrOrInt(_GenericListNode[int | str], listof=(IntNode, StringNode)): ...


if True:  # Timestr
	from ..src.tcr_timestr import timestr_lookup

	class TimestrNodeRobostrPartNode(
		CompoundNode,
		ParsableNode[float],
		require_matched_marker=True,
		nodes=(
			FloatNode(
				"number",
				CompoundNodeMatchedMarkerNode(
					"",
					*[LiteralNode(unit, "*", IrrefutableNode()) for unit in sorted(timestr_lookup, key=len, reverse=True)],
				),
			),
		),
	):
		def parse(self):
			seconds = 0

			parsed = [x for x in self._parsed if not isinstance(x, DisposableNode)]

			for node_number_int, node_unit_literal in zip(parsed[::2], parsed[1::2], strict=True):
				match (node_number_int, node_unit_literal):
					case (ParsableNode(_, n), LiteralNode(u)):
						seconds += n * timestr_lookup[u]
					case _:
						raise RuntimeError("Invalid set of nodes")

			return seconds

	class TimestrNodeTIMEPartNode(
		CompoundNode,
		ParsableNode[datetime.time],
		require_matched_marker=True,
		nodes=(
			Hour24IntNode(
				"hours",
				DisposableLiteralNode(
					":",
					CompoundNodeMatchedMarkerNode(
						"",
						MinuteOrSecondIntNode(
							"minutes",
							DisposableLiteralNode(
								":",
								MinuteOrSecondIntNode("seconds"),
								IrrefutableNode(),
							),
							IrrefutableNode(),
						),
						IrrefutableNode(),
					),
				),
			),
		),
	):
		tzinfo: datetime.tzinfo

		def _init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.set_tzinfo()

		exec("__init__ = _init__; del _init__")

		def set_tzinfo(self, tzinfo: datetime.tzinfo = datetime.datetime.now().astimezone().tzinfo):
			self.tzinfo = tzinfo
			return self

		def parse(self):
			parsed = [x.parse() for x in self._parsed if not isinstance(x, DisposableNode)]

			h, m, s, *_ = (*parsed, 0, 0)  # Fill unspecified values with zeroes, eg. 13: -> 13:00:00

			return datetime.time(h, m, s, tzinfo=self.tzinfo)

	class TimestrNodeDATEPartNode(
		CompoundNode,
		ParsableNode[datetime.date],
		require_matched_marker=True,
		nodes=(
			DayNode(
				"days",
				DisposableLiteralNode(
					"-",
					CompoundNodeMatchedMarkerNode(
						"",
						MonthNode(
							"months",
							DisposableLiteralNode(
								"-",
								YearNode("years"),
								IrrefutableNode(),
							),
							IrrefutableNode(),
						),
						IrrefutableNode(),
					),
				),
			),
		),
	):
		tzinfo: datetime.tzinfo

		def _init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.set_tzinfo()

		exec("__init__ = _init__; del _init__")

		def set_tzinfo(self, tzinfo: datetime.tzinfo = datetime.datetime.now().astimezone().tzinfo):
			self.tzinfo = tzinfo
			return self

		def _try_parse(self, d: int, m: int, y: int) -> datetime.date | None:
			if not m or not y:
				now = datetime.datetime.now(tz=self.tzinfo)

			if not m:
				m = now.month

			if not y:
				y = now.year

			y, m, d = int(y), int(m), int(d)

			try:
				return datetime.date(y, m, d)
			except ValueError:
				return None

		def match(self, s):
			result = super().match(s)

			if result is None:
				return None

			matched, *_ = result

			d, m, y, *_ = (*matched.split("-"), "", "")

			if self._try_parse(d, m, y) is None:
				return None

			return result

		def parse(self):
			parsed = [x.parse() for x in self._parsed if not isinstance(x, DisposableNode)]

			d, m, y, *_ = (*parsed, "", "")  # Fill unspecified values with zeroes, eg. 13: -> 13:00:00

			return self._try_parse(d, m, y)

	class TimestrNode(
		CompoundNode,
		ParsableNode[float],
		nodes=(
			UnreachableNode(
				"junc",
				KeywordNode(
					"!",
					"*",
				),
			),
			TimestrNodeTIMEPartNode(
				"",
				CompoundNodeMatchedMarkerNode("", "junc/*", IrrefutableNode()),
			),
			TimestrNodeDATEPartNode(
				"",
				CompoundNodeMatchedMarkerNode("", "junc/*", IrrefutableNode()),
			),
			TimestrNodeRobostrPartNode(
				"",
				CompoundNodeMatchedMarkerNode("", "junc/*", IrrefutableNode()),
			),
		),
	):
		def _init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.set_tzinfo()

		exec("__init__ = _init__; del _init__")

		def set_tzinfo(self, tzinfo: datetime.tzinfo = datetime.datetime.now().astimezone().tzinfo):
			for node in self.children:
				if hasattr(node, "set_timezone"):
					node.set_timezone(tzinfo)
			return self

		def match(self, s):
			result = super().match(s)

			if len(tuple(x for x in self._parsed if isinstance(x, TimestrNodeTIMEPartNode))) > 1:
				return None

			return result

		def parse(self, *, tzinfo: datetime.tzinfo = datetime.datetime.now().astimezone().tzinfo):
			parsed = (x for x in self._parsed if not isinstance(x, DisposableNode))

			seconds = 0

			node_time_result = None
			node_date_result = None

			for node in parsed:
				match node:
					case TimestrNodeRobostrPartNode(_, value):
						seconds += value
					case TimestrNodeTIMEPartNode(_, value):
						# Guaranteed to ever be only 1 or 0 of them, due to TimestrNode.match()
						node_time_result = value
					case TimestrNodeDATEPartNode(_, value):
						# Guaranteed to ever be only 1 or 0 of them, due to TimestrNode.match()
						node_date_result = value
					case n:
						raise RuntimeError(f"[BUG] Unknown node: {n!r}")

			if node_time_result is None or node_date_result is None:
				now = datetime.datetime.now(tz=tzinfo)

			if node_time_result is None:
				node_time_result = (now.hour, now.minute, now.second)

			if node_date_result is None:
				node_date_result = (now.year, now.month, now.day)

			return seconds
