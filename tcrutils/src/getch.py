import os
from collections.abc import Generator as _Generator

if os.name == "nt":
	import msvcrt
else:
	import sys
	import termios
	import tty


class _KeyCodeBase:
	display_char_d: dict[str, str]

	def __init__(self):
		self.display_char_d = {}

	def __iter__(self):
		return (x for x in self.vars().values())

	def vars(self) -> dict[str, str]:
		return {k: v for k, v in self.__class__.__dict__.items() if k.isupper()}


class _KeyCodeSimpleType(_KeyCodeBase):
	if os.name == "nt":
		BACKSPACE = "\b"
		CTRL_BACKSPACE = "\b"  # Seems to be the same unfortunately? Cant differentiate between those :c

		WINDOWS_COMPOUND_KEYCODE_ESC_CHAR = "\xe0"
		"""(Probably) (In most cases) (i'm actually not sure) means: immediatelly following this press, there will be another, one indicating a compound keycode, for example the HOME key sends two pulses to getch, first b"\xe0" then immediately after b"G".

		This should be handled automatically by getchs()
		"""
	else:
		BACKSPACE = "\x7f"
		CTRL_BACKSPACE = "\x17"

	NULL = "\x00"

	ESC = "\x1b"

	CTRL_A = "\x01"
	CTRL_B = "\x02"
	CTRL_C = "\x03"
	CTRL_D = "\x04"
	CTRL_E = "\x05"
	CTRL_F = "\x06"
	CTRL_G = "\a"
	CTRL_H = "\b"
	CTRL_I = "\t"
	CTRL_J = "\n"
	CTRL_K = "\v"
	CTRL_L = "\f"
	CTRL_M = "\r"
	CTRL_N = "\x0e"
	CTRL_O = "\x0f"
	CTRL_P = "\x10"
	CTRL_Q = "\x11"
	CTRL_R = "\x12"
	CTRL_S = "\x13"
	CTRL_T = "\x14"
	CTRL_U = "\x15"
	CTRL_V = "\x16"
	CTRL_W = "\x17"
	CTRL_X = "\x18"
	CTRL_Y = "\x19"
	CTRL_Z = "\x1a"

	ENTER = CTRL_M
	TAB = CTRL_I

	def is_simple_ctrl(
		self,
		s: str,
		*,
		count_tab_and_enter_as_ctrl: bool = False,
		count_backspace_as_ctrl: bool = False,
	) -> bool:
		"""Is the given key, a key of the CTRL + any letter of the english alphabet (26 letters). Except Ctrl+I and Ctrl+M, since they map to the same as TAB and ENTER, though this can be adjusted via the keyword argument."""
		if count_tab_and_enter_as_ctrl:
			if s in (self.ENTER, self.TAB):
				return True

		if count_backspace_as_ctrl:
			if s == self.BACKSPACE:
				return True

		return s in (
			self.CTRL_A,
			self.CTRL_B,
			self.CTRL_C,
			self.CTRL_D,
			self.CTRL_E,
			self.CTRL_F,
			self.CTRL_G,
			# NO CTRL_H,
			# NO CTRL_I
			self.CTRL_J,
			self.CTRL_K,
			self.CTRL_L,
			# NO CTRL_M
			self.CTRL_N,
			self.CTRL_O,
			self.CTRL_P,
			self.CTRL_Q,
			self.CTRL_R,
			self.CTRL_S,
			self.CTRL_T,
			self.CTRL_U,
			self.CTRL_V,
			self.CTRL_W,
			self.CTRL_X,
			self.CTRL_Y,
			self.CTRL_Z,
		)


class _KeyCodeCompoundType(_KeyCodeBase):
	# Arrows
	if os.name == "nt":
		UP = "\0H"
		DOWN = "\0M"
		LEFT = "\0K"
		RIGHT = "\0P"
	else:
		UP = "\x1b[A"
		DOWN = "\x1b[B"
		LEFT = "\x1b[C"
		RIGHT = "\x1b[D"


class _KeyCodeType(_KeyCodeSimpleType, _KeyCodeCompoundType): ...


KeyCode = _KeyCodeType()
KeyCodeSimple = _KeyCodeSimpleType()
KeyCodeCompound = _KeyCodeCompoundType()


class _Getchs(_KeyCodeType):
	if os.name == "nt":

		def __call__(self):
			"""Reads a single character or key sequence from the keyboard."""
			first_char = msvcrt.getwch()

			if first_char in ("\x00", "\xe0"):
				second_char = msvcrt.getwch()
				return first_char + second_char
			return first_char

	else:

		def __call__(self):
			"""Reads a single character or key sequence from the keyboard."""
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(fd)
				char = sys.stdin.read(1)
				if char == "\x1b":
					return char + sys.stdin.read(2)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			return char


getchs = _Getchs()
"""Improved implementation of tcr.getch(). Able to condense compound/[containg escape sequence] keypresses into one return value."""


class _Getch:
	"""Get a single character from standard input.

	Warning: May behave differently on Unix and Windows
	"""

	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self):
		"""Get a single character from standard input.

		Warning: May behave differently on Unix and Windows
		"""
		return self.impl()


class _GetchUnix:
	def __init__(self):
		import sys
		import termios
		import tty

		self.sys = sys
		self.termios = termios
		self.tty = tty

	def __call__(self):
		fd = self.sys.stdin.fileno()
		old_settings = self.termios.tcgetattr(fd)
		try:
			self.tty.setraw(self.sys.stdin.fileno())
			ch = self.sys.stdin.read(1)
		finally:
			self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old_settings)
		return ch.encode(encoding="ascii")


class _GetchWindows:
	def __init__(self):
		import msvcrt

		self.msvcrt = msvcrt

	def __call__(self):
		return self.msvcrt.getch()


getch = _Getch()
"""Original implementation of tcr.getch(). This is (probably) strictly worse than tcr.getchs(), please use that one instead, unless you really want to deal with escape syntax..."""
