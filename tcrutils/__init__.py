"""Useful stuff for tcr projects.

Importing convention:
```py
>>> import tcrutils as tcr
```

It's also recommended to import stuff directly instead of the entire module
```py
>>> from tcrutils import timestr
```

Star-importing is fine, ctrl-click whatever you're hovering on to see __all__ if you wish.
```py
>>> from tcrutils import *
```
Joke functions and other barely useful crap is not included in star imports.
"""

from . import discord, src
from .discord.tcrd_embeds import embed
from .discord.tcrd_limits import DiscordLimits
from .discord.tcrd_string import get_token
from .src.tcr_color import c, color, colour, printc
from .src.tcr_compare import able
from .src.tcr_console import breakpoint, console
from .src.tcr_constants import *
from .src.tcr_decorator import autorun, convert, instance, test, timeit
from .src.tcr_dict import dict_zip, merge_dicts
from .src.tcr_dir import dir2, dir3
from .src.tcr_error import error  # 'tcrerror' in star imports, either in 'tcr.error'/'tcr.tcrerror'
from .src.tcr_error import error as tcrerror
from .src.tcr_extract_error import extract_error, extract_traceback
from .src.tcr_F import F
from .src.tcr_getch import getch
from .src.tcr_input import insist
from .src.tcr_int import float2int, hex, recursive_sum
from .src.tcr_iterable import (
    Or,
    batched,
    bogo_sort,
    cut_at,
    getattr_queue,
    getmanyattrs,
    hasmanyattrs,
    limited_iterable,
    shuffled,
    stalin_sort,
)
from .src.tcr_joke import christmas_tree, fizzbuzz, oddeven
from .src.tcr_language import apostrophe_s, make_plural, nth
from .src.tcr_markdown import codeblock, uncodeblock
from .src.tcr_misspellings import asert, trei
from .src.tcr_null import Null, UniqueDefault
from .src.tcr_other import intbool
from .src.tcr_path import path
from .src.tcr_print import fmt_iterable, print_block, print_iterable
from .src.tcr_regex import RegexPreset
from .src.tcr_run import RunSACAble, run_sac
from .src.tcr_sdb import ShelveDB
from .src.tcr_string import commafy
from .src.tcr_terminal import terminal
from .src.tcr_timestr import timestr
from .src.tcr_void import araiser, avoid, raiser, void

# fmt: off

__all__ = [
  "c", "color", "colour", "printc",     # color

  "console",                            # console

  "autorun", "convert",                 # decorator

  "dict_zip", "merge_dicts",            # dict

  "tcrerror",                           # error

  "extract_error", "extract_traceback", # extract_error

  "getch",                              # getch

  "batched", "cut_at", "shuffled",      # iterable
  "limited_iterable", "getattr_queue",
  "Or", "hasmanyattrs", "getmanyattrs",

  "codeblock", "uncodeblock",           # markdown

  "asert", "trei",                      # misspellings

  "Null", "UniqueDefault",              # null

  "commafy",                            # string

  "nth", "make_plural",                 # language
  "apostrophe_s",

  "hex", "float2int",                   # int

  "intbool",                            # other

  "dir2", "dir3",                       # dir

  "print_iterable", "print_block",      # print

  "RegexPreset",                        # regex

  "run_sac",                            # run

  "timestr",                            # timestr

  "insist",                             # input

  "able",                               # compare

  "DiscordLimits",                      # Discord

  "ShelveDB",                           # sdb

  "BACKSLASH",                          # constants
  "NEWLINE",
  "CARR_RET",
  "BACKSPACE",
  "BACKTICK", "BACKTICKS",
  "APOSTROPHE", "QUOTE",
  "FAKE_PIPE",
]
