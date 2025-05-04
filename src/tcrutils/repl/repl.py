import string

import colored

from ..console import console as c
from ..getch import getchs as getchs
from ..terminal import terminal
from .nodes import *
from .parser import parse_and_submit_nodes


def raise_for_not_only_nodes(nodes: tuple[Node]):
	if nodes and not all(isinstance(node, Node) for node in nodes):
		raise ValueError("nodes must be tuple[Node]")


class Repl:
	def display_node(self, n: Node, /) -> str:
		match n:
			case OwnDisplayNode():
				return n.display()
			case UnknownNode(text=text):
				return f"{colored.Style.UNDERLINE + colored.Fore.RED}{text}{FMTC._}"
			case CompoundNode():
				return "".join(self.display_node(x) for x in n._parsed)
			case Node(text=text):
				return f"{text}"
			case _:
				raise TypeError("Cannot display anything other than a Node")

	def __init__(self, *nodes: Node):
		raise_for_not_only_nodes(nodes)

		self.nodes = nodes
		self.chs_history = []
		self.chs_history_ptr = 0

	def on_ctrl(self, key: str) -> str | None:
		if key == getchs.CTRL_U:
			self.chs.clear()
			return
		if key == getchs.CTRL_C:
			raise KeyboardInterrupt

		if self.chs:
			return

		if key == getchs.CTRL_D:
			raise EOFError

	def on_arrow(self, key: str) -> str | None:
		if key == getchs.UP:
			if self.chs_history_ptr < self.chs_history.__len__() - 1:
				self.chs_history_ptr += 1
		if key == getchs.DOWN:
			if self.chs_history_ptr > 0:
				self.chs_history_ptr -= 1

	def printhook_prompt(self, last_char: str | None, *submitted_nodes: Node) -> tuple[bool, str]:
		fucked = bool(submitted_nodes and isinstance(submitted_nodes[-1], UnknownNode)) or contains_incomplete_nodes(submitted_nodes)

		chr1 = ">"

		if fucked:
			chr1 = "!"
		elif not submitted_nodes:
			chr1 = " "
		elif submitted_nodes[-1].children:
			chr1 = "+"

		chr2 = " " if chr1 != ">" else ">"

		if self.chs_history_ptr:
			chr3 = (str(self.chs_history_ptr)[-3:].__len__() - 1) * "\b" + str(self.chs_history_ptr)[-3:]

		chr3 = ">"
		return f"{chr1}{chr2}{chr3}"

	def printhook(self, last_char: str | None, *submitted_nodes: Node) -> None:
		print(f"{(terminal.width * ' ')}\r{self.printhook_prompt(last_char, *submitted_nodes)} {''.join(x.__str__() for x in submitted_nodes)}", end="\r")

	hide_cursor: bool = True
	valid_chars = string.ascii_letters + string.punctuation + string.digits + " \t" + "ąłćżźśćó"
	no_enter_on_unknown_or_incomplete: bool = True
	remove_root_node_from_output: bool = True

	@property
	def chs(self):
		return self.chs_history[self.chs_history_ptr]

	def __call__(self) -> list[Node]:
		while [] in self.chs_history:
			self.chs_history.remove([])

		self.chs_history.insert(0, [])
		self.chs_history_ptr = 0

		if self.hide_cursor:
			terminal.cursor.hide()

		self.printhook(None)

		try:
			while True:
				ch = getchs()

				if ch == getchs.ENTER:
					pass
				elif ch == getchs.BACKSPACE:
					if self.chs:
						self.chs.pop()
				elif ch == getchs.CTRL_BACKSPACE:
					if self.chs:
						while self.chs and self.chs[-1] in " \t":
							self.chs.pop()
						while self.chs and self.chs[-1] not in " \t":
							self.chs.pop()
						while self.chs and self.chs[-1] in " \t":
							self.chs.pop()
				elif ch in (getchs.UP, getchs.DOWN, getchs.LEFT, getchs.RIGHT):
					ch = self.on_arrow(ch)
				elif getchs.is_simple_ctrl(ch):
					ch = self.on_ctrl(ch)
				elif ch in self.valid_chars:
					self.chs.append(ch)

				submitted_nodes = parse_and_submit_nodes("".join(self.chs), self.nodes)

				self.printhook(ch, *submitted_nodes)

				if ch == getchs.ENTER:
					if self.no_enter_on_unknown_or_incomplete:
						if isinstance(submitted_nodes[-1], UnknownNode):
							continue

						if contains_incomplete_nodes(submitted_nodes):
							continue

					if submitted_nodes[-1].children:
						continue

					submitted_nodes = [x for x in submitted_nodes if not isinstance(x, DisposableNode)]
					submitted_nodes = [(x.convert() if isinstance(x, ConvertableNode) else x) for x in submitted_nodes]
					return submitted_nodes  # noqa: RET504
		finally:
			if self.hide_cursor:
				terminal.cursor.unhide()
