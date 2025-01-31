import pathlib as p
import sys
import threading as th
import traceback
import warnings as ws
from collections.abc import Callable

from colored import Back, Fore, Style

from .classfuncs import get_classname
from .console import console
from .iterable import cut_at
from .print import FMTC

C_WHITE = Fore.white + Style.bold
C_NUMBER = FMTC.NUMBER
C_WARNING = Fore.yellow + Style.bold
C_ERROR = Fore.red + Style.bold
C_EXCEPTION = FMTC.INTERNAL_EXCEPTION


def default_err_or_warning_printhook(s: str, warning: Warning | Exception, filename: str, lineno: int, *, tb=None) -> None:
	"""Default printhook for tcr.WarningCatcher."""
	path = p.Path(filename)

	AROUND: int = 2
	"""How many lines around the line of the warning to show."""
	CUTOFF: int = 70
	"""How many (max) characters can be shown per line until they ge..."""

	is_warning = isinstance(warning, Warning)

	color = C_WARNING if is_warning else C_ERROR

	if not path.exists():
		lines = ""
	else:
		lines = path.read_text().split("\n")
		lines = lines[max(0, lineno - (AROUND + 1)) : lineno + AROUND]
		while all(x.startswith(" ") for x in lines):
			lines = [x[1:] for x in lines]
		lines = [f"{C_NUMBER}{lineno - AROUND + i}{color} {'>' if i == AROUND else '|'}{FMTC._} {cut_at(x, CUTOFF)}" for i, x in enumerate(lines)]
		lines = "\n".join(lines)
		lines = f"\n{lines}"

	if tb:
		traceback.print_tb(tb)

	func = console.warn if is_warning else console.error
	func(f"{color}{filename}{C_WHITE}:{C_NUMBER}{lineno}{C_WHITE}: {C_EXCEPTION}{get_classname(warning)}{C_WHITE}: {color}{str(warning).replace('<locals>.', '')}{lines}")


def _errorcatcher_excepthook(type, value, traceback):
	frame = traceback.tb_frame
	filename = frame.f_code.co_filename
	lineno = frame.f_lineno
	default_err_or_warning_printhook(str(value), value, filename, lineno, tb=traceback)


class ErrorCatcher:
	def __init__(self, **kwargs) -> None:
		self.install(**kwargs)

	@staticmethod
	def install():
		sys.excepthook = _errorcatcher_excepthook


class WarningCatcher:
	"""Catches any warnings (for example "Coroutine X was not awaited") and forwards them as text to the selected (or default: tcr.console.warn) printhook.

	Usage:
	```py
	tcr.WarningCatcher()
	# OR
	tcr.WarningCatcher.install() # Tgus
	```
	"""

	@staticmethod
	def install(**kwargs):
		"""Alias for tcr.WarningCatcher(**kwargs). Use it for better typehints."""
		_WarningCatcher.install(**kwargs)

	def __init__(
		self,
		printhook: Callable[[str, Warning, str, int], None] = default_err_or_warning_printhook,
	) -> None:
		"""Catches any warnings (for example "Coroutine X was not awaited") and forwards them as text to the selected (or default: tcr.console.warn) printhook.

		Usage:
		```py
		tcr.WarningCatcher()
		```

		Args:
		        - printhook: Callable[[str, Warning, str, int], None], Defines a printer function, for more info see this module's default_showwarning_printhook function and https://docs.python.org/3/library/warnings.html#warnings.showwarning.
		"""
		_WarningCatcher.install(
			printhook=printhook,
		)


class _WarningCatcher(th.Thread):
	_initiated = False
	_installed = False

	def __init__(self, *, printhook):
		if _WarningCatcher._initiated:
			raise RuntimeError("WarningCatcher can only be initiated once.")
		super().__init__()
		_WarningCatcher._initiated = True
		self.__printhook = printhook
		self.daemon = True
		self._stop_event = th.Event()

	def run(self):
		def showwarning(message, category, filename, lineno, file=None, line=None):
			self.__printhook(str(message), message, filename, lineno)

		with ws.catch_warnings():
			ws.showwarning = showwarning
			while not self._stop_event.is_set():
				self._stop_event.wait(0.1)  # Check every 0.1 second for the stop signal

	def stop(self):
		self._stop_event.set()

	@classmethod
	def install(cls, **kwargs):
		if _WarningCatcher._installed:
			raise RuntimeError("WarningCatcher can only be installed once.")
		_WarningCatcher._installed = True

		catcher = cls(**kwargs)
		catcher.start()
		return catcher
