"""Useful stuff for tcr projects.

Importing convention:
```py
>>> import tcrutils as tcr
```

It's also recommended to import stuff directly instead of the entire module
```py
>>> from tcrutils import timestr
```

~~Star-importing is fine, ctrl-click whatever you're hovering on right now to see __all__ if you wish.~~
Update: neeevermind there's just so much stuff you better import directly. __all__ is still maintained tho...
```py
>>> from tcrutils import *
```
Joke functions and other barely useful crap are not included in star imports.
"""

try:
  from .discord.tcrd_embeds import embed, modal
except ImportError: ...
from . import discord, imgui, src
from . import discord as D
from . import dr as dynamic_responses
from . import dr as execute
from ._version import __version__
from .discord.tcrd_limits import DiscordLimits
from .discord.tcrd_string import get_token
from .dr import placeholder_set as dr_placeholder_sets
from .dr import placeholders as dr_placeholders
from .src import tcr_ensure_deps as ensure_depencencies
from .src import tcr_joke as joke
from .src import tcr_types as types
from .src import tcr_zoo as zoo
from .src.tcr_b64 import b64
from .src.tcr_class import DefaultsGetAttr, DefaultsGetItem, DefaultsGetSetAttr, DefaultsGetSetItem, NoInit, Singleton, partial_class
from .src.tcr_classfuncs import get_classname, get_name_classname, get_qualname_classname
from .src.tcr_compare import able, isdunder
from .src.tcr_console import breakpoint, console, start_eval_session
from .src.tcr_console import console as c
from .src.tcr_constants import *
from .src.tcr_context import random_seed_lock
from .src.tcr_decorator import autorun, convert, copy_kwargs, instance, skip_first_call, skip_first_call_async, test, timeit, with_overrides
from .src.tcr_dev import generate_function_argument_typehints, generate_type_hinter
from .src.tcr_dict import DotDict, JSDict, JSDotDict, clean_dunder_dict, dict_zip, merge_dicts
from .src.tcr_dir import dir2, dir3
from .src.tcr_error import error  # 'tcrerror' in star imports, either in 'tcr.error'/'tcr.tcrerror'
from .src.tcr_error import error as tcrerror
from .src.tcr_extract_error import extract_error, extract_traceback
from .src.tcr_F import F
from .src.tcr_getch import getch
from .src.tcr_inject import ErrorCatcher, WarningCatcher
from .src.tcr_input import insist
from .src.tcr_inspect import get_file_colon_lineno, get_lineno
from .src.tcr_int import clamp, float2int, hex, recursive_sum
from .src.tcr_iterable import Or, batched, bogo_sort, cut_at, getattr_queue, getmanyattrs, hasmanyattrs, limited_iterable, shuffled, stalin_sort
from .src.tcr_language import apostrophe_s, make_plural, nth, plural_s
from .src.tcr_markdown import codeblock, codeblocks, discord_error, uncodeblock
from .src.tcr_misspellings import asert, trei
from .src.tcr_null import Null, Undefined, UniqueDefault
from .src.tcr_other import intbool
from .src.tcr_overload import Overload, OverloadMeta, overload
from .src.tcr_path import path
from .src.tcr_print import alert, fmt_iterable, print_block, print_iterable
from .src.tcr_regex import RegexPreset
from .src.tcr_run import RunSACAble, run_sac
from .src.tcr_sdb import ShelveDB
from .src.tcr_string import SlashableString, commafy, custom_zfill, join_urlstr, polaris_progressbar
from .src.tcr_temp import temp_file
from .src.tcr_terminal import terminal
from .src.tcr_test import asshole, raises, rashole
from .src.tcr_timestr import TStr, t_day, t_hour, t_minute, t_week, t_year, timestr
from .src.tcr_uptime import Uptime
from .src.tcr_void import araiser, avoid, raiser, void

# fmt: off

__all__ = [
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

  "Null", "Undefined", "UniqueDefault", # null

  "commafy",                            # string

  "nth", "make_plural",                 # language
  "apostrophe_s",

  "hex", "float2int",                   # int

  "intbool",                            # other

  "dir2", "dir3",                       # dir

  "print_iterable", "print_block",      # print
  "fmt_iterable",

  "RegexPreset",                        # regex

  "run_sac",                            # run

  "timestr",                            # timestr

  "insist",                             # input

  "able",                               # compare

  "DiscordLimits",                      # Discord

  "ShelveDB",                           # sdb

  "Overload", "overload",               # overload

  "BACKSLASH",                          # constants
  "NEWLINE",
  "CARR_RET",
  "BACKSPACE",
  "BACKTICK", "BACKTICKS",
  "APOSTROPHE", "QUOTE",
  "FAKE_PIPE",
]
