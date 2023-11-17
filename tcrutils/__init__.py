"""Useful stuff for tcr projects."""

from .src.tcr_color import c, color, colour, printc
from .src.tcr_console import breakpoint, console
from .src.tcr_constants import *
from .src.tcr_constants import __all__ as _all_constants
from .src.tcr_decorator import autorun, convert, test, timeit
from .src.tcr_dict import dict_zip, merge_dicts
from .src.tcr_error import error
from .src.tcr_extract_error import extract_error
from .src.tcr_F import F
from .src.tcr_getch import getch
from .src.tcr_iterable import batched, cut_at
from .src.tcr_markdown import codeblock, uncodeblock
from .src.tcr_misspellings import asert, trei
from .src.tcr_null import Null
from .src.tcr_other import commafy, fizzbuz, hex, intbool, oddeven
from .src.tcr_path import path
from .src.tcr_print_iterable import print_iterable
from .src.tcr_regex import RegexPreset
from .src.tcr_run import RunSACAble, run_sac
from .src.tcr_timestr import timestr

# fmt: off
__all__ = [
  "c", "color", "colour", "printc", # color
  "console",                        # console
  "autorun", "convert",             # decorator
  "dict_zip", "merge_dicts",        # dict
  "extract_error",                  # extract_error
  "getch",                          # getch
  "batched", "cut_at",              # iterable
  "codeblock", "uncodeblock",       # markdown
  "asert", "trei",                  # misspellings
  "Null",                           # null
  "commafy", "hex", "intbool",      # other
  "path",                           # path
  "print_iterable",                 # print_iterable
  "RegexPreset",                    # regex
  "run_sac",                        # run
  "timestr",                        # timestr

  "BACKSLASH",                      # constants
  "NEWLINE",
  "CARR_RET",
  "BACKSPACE",
  "BACKTICK", "BACKTICKS",
  "APOSTROPHE", "QUOTE",
  "FAKE_PIPE",
  "DiscordLimits",
]
