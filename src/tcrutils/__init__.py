"""# Useful stuff for tcr projects.

```
>>> from tcrutils.{feature_module} import feature
```

### Nyaaa :3

```
>>> from tcrutils.print import gay
>>> print(gay('nyaaaaa')) # uwu :3
```
"""

from ._version import __version__

__tcr_rainbow__ = True


if 0:  # A crude performance-measuring function
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


if False:  # Left `if False`d out for archival purposes (yeah.. there's git but i like it being here :3 uwu)
	from . import case as case
	from . import ensure_deps as ensure_depencencies
	from . import joke as joke
	from . import path, repl
	from . import types as types
	from .b64 import decode as b64d
	from .b64 import encode as b64e
	from .class_ import CachedInstancesMeta, DefaultsGetAttr, DefaultsGetItem, DefaultsGetSetAttr, DefaultsGetSetItem, NoInit, Singleton, new_cell, partial_class
	from .classfuncs import get_classname, get_name_classname, get_qualname_classname
	from .codeblock import codeblock, codeblocks, uncodeblock
	from .compare import able, able_simple, able_simple_result, isdunder
	from .console import breakpoint, console, start_eval_session
	from .console import console as c
	from .context import random_seed_lock
	from .decorator import copy_kwargs, copy_kwargs_sunder, skip_first_call, skip_first_call_async, test, timeit, with_overrides
	from .dev import generate_function_argument_typehints, generate_type_hinter
	from .dict import DotDict, clean_dunder_dict, dict_zip, merge_dicts
	from .dir import dir2, dir3, dir_recursive, vars2, vars3, vars_recursive
	from .extract_error import extract_error, extract_traceback, module_error_map, modules_error_map, print_exception_with_traceback
	from .getch import KeyCode, KeyCodeCompound, KeyCodeSimple, getch, getchs
	from .import_ import load_package_dynamically
	from .inject import ErrorCatcher, WarningCatcher
	from .input import insist
	from .inspect import eval_fback, get_file_colon_lineno, get_lineno
	from .int import clamp, float2int, hex, recursive_sum
	from .iterable import Or, batched, bogo_sort, cut_at, getattr_queue, getmanyattrs, hasmanyattrs, limited_iterable, shuffled, slice_between, stalin_sort
	from .language import apostrophe_s, make_plural, nth, plural_s
	from .misspellings import asert
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
