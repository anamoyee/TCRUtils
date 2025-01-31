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

if False:
	import time

	def b(s=""):
		if not hasattr(b, "t"):
			b.t = time.perf_counter()
			b.s = 0
			return
		t1 = b.t
		t2 = time.perf_counter()

		t = t2 - t1
		b.s += t

		print(f"{s:10} {t:.10f}")
		b.t = time.perf_counter()


from . import case as case
from . import ensure_deps as ensure_depencencies
from . import joke as joke
from . import repl
from . import types as types
from ._version import __version__
from .b64 import b64
from .class_ import CachedInstancesMeta, DefaultsGetAttr, DefaultsGetItem, DefaultsGetSetAttr, DefaultsGetSetItem, ErrDenoted, NoInit, Singleton, new_cell, partial_class
from .classfuncs import get_classname, get_name_classname, get_qualname_classname
from .compare import able, able_simple, able_simple_result, isdunder
from .console import breakpoint, console, start_eval_session
from .console import console as c
from .constants import *
from .context import random_seed_lock
from .decorator import autorun, convert, copy_kwargs, copy_kwargs_sunder, instance, skip_first_call, skip_first_call_async, test, timeit, with_overrides
from .dev import generate_function_argument_typehints, generate_type_hinter
from .dict import DotDict, JSDict, JSDotDict, clean_dunder_dict, dict_zip, merge_dicts
from .dir import dir2, dir3, dir_recursive, vars2, vars3, vars_recursive
from .error import error
from .extract_error import extract_error, extract_traceback, module_error_map, modules_error_map, print_exception_with_traceback
from .F import F
from .getch import KeyCode, KeyCodeCompound, KeyCodeSimple, getch, getchs
from .import_ import load_package_dynamically
from .inject import ErrorCatcher, WarningCatcher
from .input import insist
from .inspect import eval_fback, get_file_colon_lineno, get_lineno
from .int import clamp, float2int, hex, recursive_sum
from .iterable import Or, batched, bogo_sort, cut_at, getattr_queue, getmanyattrs, hasmanyattrs, limited_iterable, shuffled, slice_between, stalin_sort
from .language import apostrophe_s, make_plural, nth, plural_s
from .misspellings import asert, trei
from .null import Null, Undefined, UniqueDefault
from .other import intbool
from .overload import Overload, OverloadMeta, overload
from .path import path
from .print import FMT_BRACKETS, FMTC, alert, fmt_iterable, gay, print_block, print_iterable
from .regex import RegexPreset
from .result import Result, ResultUnwrappedErrOnValueError, ResultUnwrappedOnErrorError
from .run import RunSACAble, run_sac
from .sdb import ShelveDB
from .string import SlashableString, commafy, custom_zfill, get_token, join_urlstr, polaris_progressbar
from .temp import temp_file
from .terminal import terminal
from .test_ import ass, raises, rass
from .timestr import TStr, t_day, t_hour, t_minute, t_week, t_year, timestr
from .typehints import force_keyword_only_typehints
from .uptime import Uptime
from .void import alambda, araiser, avoid, raiser, void

# fmt: off

__tcr_rainbow__ = True

__all__ = [  # noqa: RUF022
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
