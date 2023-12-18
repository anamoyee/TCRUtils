"""Useful stuff for tcr projects.

Importing convention:
```py
>>> import tcrutils as tcr
```

It's also recommended to import stuff directly instead of the entire module
```py
>>> from tcrutils import timestr
```

Star-importing is fine, check __init__.py to see __all__.
```py
>>> from tcrutils import *
>>> timestr
<Timestr object at ...> # Fine, no errors, timestr is included in __all__
>>> fizzbuzz
NameError: name 'fizzbuzz' is not defined # fizzbuzz is not included in __all__, use tcr.fizzbuzz or from tcrutils import fizzbuzz
"""

from .src.tcr_color import c, color, colour, printc
from .src.tcr_console import breakpoint, console
from .src.tcr_constants import *
from .src.tcr_decorator import autorun, convert, instance, test, timeit
from .src.tcr_dict import dict_zip, merge_dicts
from .src.tcr_error import error
from .src.tcr_error import error as tcrerror
from .src.tcr_extract_error import extract_error, extract_traceback
from .src.tcr_F import F
from .src.tcr_getch import getch
from .src.tcr_iterable import batched, bogo_sort, cut_at, shuffled, stalin_sort
from .src.tcr_markdown import codeblock, uncodeblock
from .src.tcr_misspellings import asert, trei
from .src.tcr_null import Null
from .src.tcr_other import commafy, dir2, dir3, fizzbuzz, hex, intbool, nth, oddeven, print_block
from .src.tcr_path import path
from .src.tcr_print_iterable import print_iterable
from .src.tcr_regex import RegexPreset
from .src.tcr_run import RunSACAble, run_sac
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
  "codeblock", "uncodeblock",           # markdown
  "asert", "trei",                      # misspellings
  "Null",                               # null
  "commafy", "hex", "intbool",          # other
  "print_block", "dir2", "dir3",        # other
  "print_iterable",                     # print_iterable
  "RegexPreset",                        # regex
  "run_sac",                            # run
  "timestr",                            # timestr

  "BACKSLASH",                          # constants
  "NEWLINE",
  "CARR_RET",
  "BACKSPACE",
  "BACKTICK", "BACKTICKS",
  "APOSTROPHE", "QUOTE",
  "FAKE_PIPE",
  "DiscordLimits",
]
