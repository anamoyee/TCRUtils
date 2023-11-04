"""Useful stuff for tcr projects."""

from .src.tcr_color import c, color, colour
from .src.tcr_console import console
from .src.tcr_dict import dict_zip, merge_dicts
from .src.tcr_extract_error import extract_error
from .src.tcr_null import Null
from .src.tcr_print_iterable import print_iterable
from .src.tcr_timestr import timestr

__all__ = [x for x in globals() if not x.startswith('_') and x != 'src']

from .src.tcr_decorator import autorun, test, timeit
from .src.tcr_error import error
from .src.tcr_F import F
from .src.tcr_other import oddeven
