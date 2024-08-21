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
Update: neeevermind there's just so much stuff you better import directly.
```py
>>> from tcrutils import *
```
Joke functions and other barely useful crap are not included in star imports.
"""

from types import ModuleType as __ModuleType


def __getattr__(name: str) -> __ModuleType:
  """Map `tcr.discord` to tcrdiscord (separate pip-installable module). This does not install the module via pip, only prompts you to do so if it cant be imported.

  This is done for backwards-compatibility, for fresh projects use tcrdiscord or equivalent, not tcr.discord.
  """
  # Triggers only when an attr can't be found already, so this is not called when you use like, tcr.console becasuse console is defined
  pair = {
    'discord': ('tcrdiscord', 'tcrdiscord'),
  }.get(name)

  if pair is None:
    raise AttributeError(f'AttributeError: module {__name__!r} has no attribute {name!r}')

  import_name, pip_name = pair


  import warnings
  warnings.warn(f"Accessing subpackages of tcrutils as tcr.<name> (tcr.{name}) is deprecated. Do this instead:\n\n$ pip install {pip_name}\n\n>>> import {import_name}\n", DeprecationWarning, stacklevel=2)

  try:
    return __import__(import_name)
  except ImportError as e:
    raise ImportError(f'Unable to locate pip-installable tcrutils submodule: {import_name!r}, please install it with by running the following command:\n\n$ pip install {pip_name}') from e

from . import dr, src
from . import dr as execute
from ._version import __version__
from .src import tcr_case as case
from .src import tcr_ensure_deps as ensure_depencencies
from .src import tcr_joke as joke
from .src import tcr_types as types
from .src.tcr_b64 import b64
from .src.tcr_class import CachedInstancesMeta, DefaultsGetAttr, DefaultsGetItem, DefaultsGetSetAttr, DefaultsGetSetItem, ErrDenoted, NoInit, Singleton, partial_class
from .src.tcr_classfuncs import get_classname, get_name_classname, get_qualname_classname
from .src.tcr_compare import able, isdunder
from .src.tcr_console import breakpoint, console, start_eval_session
from .src.tcr_console import console as c
from .src.tcr_constants import *
from .src.tcr_context import random_seed_lock
from .src.tcr_decorator import autorun, convert, copy_kwargs, instance, skip_first_call, skip_first_call_async, test, timeit, with_overrides
from .src.tcr_dev import generate_function_argument_typehints, generate_type_hinter
from .src.tcr_dict import DotDict, JSDict, JSDotDict, clean_dunder_dict, dict_zip, merge_dicts
from .src.tcr_dir import dir2, dir3, dir_recursive, vars2, vars3, vars_recursive
from .src.tcr_error import error
from .src.tcr_extract_error import extract_error, extract_traceback, module_error_map, modules_error_map
from .src.tcr_F import F
from .src.tcr_getch import getch
from .src.tcr_import import load_package_dynamically
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
from .src.tcr_print import alert, double_quoted_repr, fmt_iterable, gay, print_block, print_iterable
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

exec((lambda __: ''.join(chr((ord(_) - 78) % 26 + 65) if chr(65) <= _ <= chr(90) else chr((ord(_) - 84) % 26 + 97) if chr(97) <= _ <= chr(122) else _ for _ in __))(")lfEt[e<nHjwxL*\\*J ,,5)5'NftyGv2gHh>e)phg 'N(<tYa0vXedggF}l-nnTb.<furic[lig`(Fr0ySo>n}e8rNg\\v=_2g4z4sK DaXe;h/gsrbe: 5 q\nv:7)ifGt\\eEnqj9xV*<*? O,pr~y+oBnWeqrKgxvf_zgDzisI(0_B_1gYz3s{_=e`p<g}_h_F xs2rwqw\n]\ns.+.(.bfqhZb[v+pCvPyznkz/ =ggb,a# )fFvm mfpvfunG9 y#?"[::2][::-1]))

__all__ = [
  "console",                            # console

  "autorun", "convert",                 # decorator

  "dict_zip", "merge_dicts",            # dict

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
