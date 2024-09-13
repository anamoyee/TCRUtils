import datetime as dt
import pathlib
import re as regex
import sys
import typing
from enum import Enum, EnumMeta
from functools import partial, wraps
from types import GeneratorType, UnionType
from typing import Any
from typing import get_args as unpack_union
from warnings import warn

from .tcr_path import path as tcr_path_utils

try:
    from hikari.internal.enums import Enum as _HikariEnum
except ModuleNotFoundError:
    _HikariEnum = None

from _collections_abc import (
    Callable,
    Iterable,
    Mapping,
    bytearray_iterator,
    bytes_iterator,
    coroutine,
    dict_itemiterator,
    dict_items,
    dict_keyiterator,
    dict_keys,
    dict_valueiterator,
    dict_values,
    list_iterator,
    list_reverseiterator,
    longrange_iterator,
    range_iterator,
    set_iterator,
    str_iterator,
    tuple_iterator,
    zip_iterator,
)

from colored import Back, Fore, Style

try:
    from pydantic import BaseModel as PydanticBM
except ImportError:
    exec("PydanticBM = None")

from .tcr_compare import able
from .tcr_constants import NEWLINE
from .tcr_extract_error import extract_error
from .tcr_int import hex as tcrhex
from .tcr_iterable import Or, getattr_queue, limited_iterable
from .tcr_null import Null, Undefined
from .tcr_types import BrainfuckCode, GayString, QuotelessString


def double_quoted_repr(s: str, *, quote_char: str = '"'):
    """Return a string that is the same as `s` but always uses `quote_char` instead of single or double quotes on string boundaries. Make sure to correctly escape every character if needed so there are no edge cases that might break the result."""
    assert quote_char in ('"', "'")
    result = quote_char
    for char in s:
        if char in "\\" + quote_char:
            result += "\\" + char
        else:
            result += char
    return result + quote_char


def print_block(
    text: str,
    border_char: str = "#",
    *,
    margin: int = 1,
    border: int = 3,
    padding: int = 0,
    padding_top: int = 1,
    padding_bottom: int = 1,
    text_color: str = Fore.YELLOW + Style.bold,
    border_color: str = Fore.WHITE + Style.bold,
    raw: bool = False,
    allow_invalid_config: bool = False,
) -> str | None:
    """Print or return a string of a "comment-like" block with text. Colors may optionally be set to `''` (empty string) to skip coloring of that part. Ends with a color reset unless none of the colors are enabled (both set to `''`).

    Params:
        - `margin`: The amount of spaces between the text and the inner walls (left-right only)
        - `border`: The width of walls (number of border_char characters, left-right only)
        - `padding`: The number of extra spaces added to the left of each line (left side only)
        - `padding_top` & `padding_bottom`: How many '\\n' characters to add at the beginning and the end of the string (top-bottom only)
    """

    text = str(text)

    if not allow_invalid_config and margin < 0 or border < 0 or padding < 0:
        msg = f"Invalid margin, border and/or padding(s) configuration {(margin, border, padding, padding_top, padding_bottom)!r}. Override this by passing in allow_invalid_config=True"
        raise ValueError(msg)

    if not allow_invalid_config and len(border_char) != 1:
        msg = f"border_char must be 1 character long (got {border_char!r} which is {len(border_char)!r} characters long). Override this by passing in allow_invalid_config=True"
        raise ValueError(msg)

    reset = Style.reset

    if not text_color and not border_color:
        reset = ""

    bar = f"{border_char * (border + margin + len(text) + margin + border)}"
    block = f"""
{padding_top * NEWLINE}{padding * " "}{reset}{border_color}{bar}
{padding * " "}{border * border_char}{reset}{margin * " "}{text_color}{text}{reset}{margin * " "}{border_color}{border * border_char}
{padding * " "}{bar}{reset}{padding_bottom * NEWLINE}
"""[1:-1]
    if raw:
        return block

    print(block)
    return None


if True:  # \/ # fmt & print iterable
    # fmt: off
    # Format Colors, name kept short so lines don't get THAT long if this thing is used like 10 times in a single fstring
    class FMTC:
      _                   = Style.reset # Reset
      NUMBER              = Fore.BLUE + Style.bold
      TYPE                = Fore.BLUE + Style.bold
      DECIMAL             = Fore.WHITE + Style.bold
      BRACKET             = Fore.CYAN + Style.bold
      STRING              = Style.reset + Fore.YELLOW
      QUOTES              = Fore.WHITE #+ Style.bold
      COLON               = Fore.orange_1 + Style.bold
      ASTERISK            = Fore.orange_1 + Style.bold
      COROUTINE           = Fore.orange_1 + Style.bold
      FUNCTION            = Fore.orange_1 + Style.bold
      COMPLEX             = Fore.orange_1 + Style.bold
      COMMA               = Fore.dark_gray + Style.bold
      PIPE                = Fore.dark_gray + Style.bold
      SLASH               = Fore.dark_gray + Style.bold
      UNKNOWN             = Fore.dark_gray + Style.bold
      TRUE                = Fore.GREEN + Style.bold
      FALSE               = Fore.RED + Style.bold
      NULL                = Fore.dark_gray + Style.bold
      UNDEFINED           = Fore.dark_gray + Style.bold
      NONE                = Fore.light_gray + Style.bold
      BYTESTR_B           = Fore.RED + Style.bold
      ITER_I              = Fore.red_3b + Style.bold
      SPECIAL             = Fore.purple_1b + Style.bold
      INTERNAL_EXCEPTION  = Fore.red_3b + Style.bold
      BUILT_IN_EXCEPTION  = Fore.BLUE + Style.bold
      MODULE              = Fore.orange_1 + Style.bold

    class FMT_LETTERS:
      b    = f'{FMTC.BYTESTR_B}b'
      i    = f'{FMTC.ITER_I}i{FMTC._}'
      F    = f'{FMTC.SPECIAL}F'
      K    = f'{FMTC.SPECIAL}K'
      V    = f'{FMTC.SPECIAL}V'
      I    = f'{FMTC.SPECIAL}I'
      C    = f'{FMTC.COROUTINE}C'
      META = f'{FMTC.SPECIAL}Meta'

    # Format Brackets templates.
    # (FMT_BRACKETS[_t][syntax_highlighting: bool] % content) -> attaches brackets to the content with respect to syntax highlighting
    FMT_BRACKETS: dict[type | None, tuple[str, str]] = { # Format Brackets
    None:          ('[%s]',            f'{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
    list:          ('[%s]',            f'{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
    dict_keys:     ('[%s]',            f'{FMT_LETTERS.K}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
    dict_values:   ('[%s]',            f'{FMT_LETTERS.V}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
    dict_items:    ('[%s]',            f'{FMT_LETTERS.I}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
    set:           ('{%s}',            f'{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
    frozenset:     ('frozenset({%s})', f'{FMT_LETTERS.F}{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
    dict:          ('{%s}',            f'{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
    Mapping:       ('{%s}',            f'{FMTC.BRACKET}{{{FMTC._}%s{FMTC.BRACKET}}}{FMTC._}'),
    tuple:         ('(%s)',            f'{FMTC.BRACKET}({FMTC._}%s{FMTC.BRACKET}){FMTC._}'),
    GeneratorType: ('[%s]',            f'{FMTC.BRACKET}<{FMTC._}%s{FMTC.BRACKET}>{FMTC._}'),
    range:         ('range([%s])',     f'{FMTC.BRACKET}<{FMTC._}%s{FMTC.BRACKET}>{FMTC._}'),
    bytearray:     ('bytearray([%s])', f'{FMT_LETTERS.b}{FMTC.BRACKET}[{FMTC._}%s{FMTC.BRACKET}]{FMTC._}'),
    coroutine:     ('coroutine_%s',    f'{FMT_LETTERS.C}{FMTC.DECIMAL}\'{FMTC.FUNCTION}%s')
  }

    FMT_TOO_DEEP = ('[ ... ]', f'{FMTC.BRACKET}[ {FMTC.DECIMAL}... {FMTC.BRACKET}]{FMTC._}')
    """FMT_TOO_DEEP[syntax_highlighting: bool] -> attaches '[ ... ]' to the content with respect to syntax highlighting"""

    FMT_UNION_SEPARATOR = ('|', f'{FMTC.PIPE} | {FMTC._}')
    """FMT_UNION_SEPARATOR[syntax_highlighting: bool] -> attaches ' | ' to the content with respect to syntax highlighting"""

    FMT_ITER = ('iter(%s)', f'{FMT_LETTERS.i}%s')
    """(FMT_ITER[syntax_highlighting: bool] % content) -> attaches 'i' or 'iter()' to the content with respect to syntax highlighting"""

    FMT_UNKNOWN = ('%s(%s)', f'{FMTC.UNKNOWN}%s({FMTC._}%s{FMTC.UNKNOWN}){FMTC._}')
    """(FMT_UNKNOWN[syntax_highlighting: bool] % (name, content)) -> attaches name and content to an unknown object"""

    FMT_INTERNAL_EXCEPTION = ("An exception occured while trying to display this item (%s).", f"{FMTC.INTERNAL_EXCEPTION}An exception occured while trying to display this item ({FMTC.UNKNOWN}%s{FMTC.INTERNAL_EXCEPTION}).{FMTC._}")
    """(FMT_EXCEPTION[syntax_highlighting: bool] % getattr_queue(obj, '__name__', '__class__.__name__') -> Self explainatory"""

    FMT_CLASS = ("%s(%s)", f"{FMTC.TYPE}%s{FMTC.BRACKET}({FMTC._}%s{FMTC.BRACKET}){FMTC._}")
    """(FMT_CLASS[syntax_highlighting: bool]) % (getattr_queue(obj, '__name__', '__class__.__name__'), this(it))"""

    FMT_ENUM = ('%s.%s=%s', f'{FMTC.TYPE}%s{FMTC.COMMA}.{FMTC._}{Fore.WHITE}%s{FMTC.COMMA}: {FMTC._}%s')
    """(FMT_ENUM[syntax_highlighting: bool]) % (classname, valuename, this(value))"""

    FMT_ENUM_NO_CLASS = ('%s=%s', f'{FMTC._}{Fore.WHITE}%s{FMTC.COMMA}: {FMTC._}%s')
    """(FMT_ENUM_NO_CLASS[syntax_highlighting: bool]) % (valuename, this(value))"""

    FMT_ENUM_AUTO = ('%s.%s', f'{FMTC.TYPE}%s{FMTC.COMMA}.{FMTC._}{Fore.WHITE}%s')
    """(FMT_ENUM_AUTO[syntax_highlighting: bool]) % (classname, valuename)"""

    FMT_ENUM_AUTO_NO_CLASS = ('%s', f'{FMTC._}{Fore.WHITE}%s')
    """(FMT_ENUM_AUTO_NO_CLASS[syntax_highlighting: bool]) % valuename"""

    FMT_ASTERISK = ('*', f'{FMTC.ASTERISK}*')
    """FMT_ASTERISK[syntax_highlighting: bool]"""

    FMT_SYS_VERSION_INFO = f'{FMTC.COLON}Python {FMTC.COMMA}v{FMTC.DECIMAL}%s{FMTC.COMMA}.{FMTC.DECIMAL}%s{FMTC.COMMA}.{FMTC.DECIMAL}%s'
    """FMT_SYS_VERSION_INFO % sys.version_info[:3] # :3"""

    # fmt: on

    class _OverflowClass:
        amount: int

        def __init__(self, amount) -> None:
            self.amount = amount

        def __str__(self) -> str:
            return str(self.amount) if self.amount != -1 else "?"

    def _reset_return_wrapper(func):
        @wraps(func)
        def wrapper(*args, append_syntax_reset: bool = True, **kwargs):
            if kwargs.get("syntax_highlighting") and append_syntax_reset:
                s = f"{FMTC._}{func(*args, **kwargs)}{FMTC._}"

                for v in vars(FMTC).values():  # Clear any duplicate, side-by-side color tags.
                    if not isinstance(v, str):
                        continue

                    _2v = 2 * v
                    while _2v in s:
                        s = s.replace(_2v, v)

                return s
            return func(*args, **kwargs)

        return wrapper

    def _non_double_repr(obj: object, /) -> str:
        rep = repr(obj)

        if not rep:
            return rep

        if not hasattr(obj, "__class__"):
            return rep

        if not hasattr(obj.__class__, "__name__"):
            return rep

        if rep.removeprefix(obj.__class__.__name__) == rep:
            return rep

        if not rep.removeprefix(obj.__class__.__name__):
            return ""

        if rep.removeprefix(obj.__class__.__name__)[0] != "(":
            return rep

        if rep[-1] != ")":
            return rep

        return rep[(len(obj.__class__.__name__) + 1) : -1]

    def _is_enum_auto(enum_class: EnumMeta) -> bool:
        """Whether enum seems to be made with all variants `= auto()`.

        If the values are all ints and they are in either of the patterns:
        - [1, 2, 3, ...] (each number is 1 more than the previous, starting at 1)
        - [1, 2, 4, 8, 16, ...] (each number is a consecutive power of 2 (for example the idx=0 element must be 2**0 and idx=1 must be 2**1, etc.), starting at 1)

        ...If any of those patterns match, the enum is considered being made with `auto()`
        """

        variants = list(enum_class)

        values = [x.value for x in variants]

        if all(x == i for i, x in enumerate(values)):
            return True

        if all(x == (i + 1) for i, x in enumerate(values)):
            return True

        return bool(all(x == 2**i for i, x in enumerate(values)))

    def _fmt_module_highlighted(name: str, path: str | None, namespace: str | None) -> str:
        s = f"{FMTC.MODULE}{name}"
        if namespace:
            s += FMT_BRACKETS[tuple][True] % f"{FMTC.MODULE}{namespace}"
        if path:
            path = path.replace("\\\\", "\\")
            if "/" not in path:
                path = path.replace("\\", "/")
            path = fmt_iterable(path if " " in path else QuotelessString(path), syntax_highlighting=True)
            s += f"{FMTC.DECIMAL}@{path}"
        return s

    def _fmt_unknown_highlighted(it: object, /, queue_name: str) -> str:
        if match := regex.match(r"<module '(?P<module_name>[^']+)'(?: from '(?P<path>[^']+)')?(?: \((?P<namespace>[^)]+)\))?>", repr(it)):
            d = match.groupdict()

            name = d["module_name"]
            path = d["path"]
            if path is not None:
                path = tcr_path_utils.convert_to_relative_pathstr(path)
            namespace = d["namespace"]

            return _fmt_module_highlighted(name, path, namespace)

        elif match := regex.match(r"^([^\d\W](?:(?:\w)|(?:\.<locals>\.)|(?:\.<globals>\.))*)\((.*)\)$", repr(it)):
            name, body = match.groups()

            return FMT_UNKNOWN[True] % (name, body)
        else:
            return FMT_UNKNOWN[True] % (
                queue_name,
                _non_double_repr(it),
            )

    def _fmt_brainfuck(text: BrainfuckCode) -> str:
        """Format a string as brainfuck.

        Assuming syntax_highlighting==True && isinstance(text, BrainfuckCode)
        """
        return str(
            text.replace("[", "#")
            .replace("<", f"{FMTC.ASTERISK}<")
            .replace(">", f"{FMTC.ASTERISK}>")
            .replace(".", f"{FMTC.DECIMAL}.")
            .replace(",", f"{FMTC.COMMA},")
            .replace("+", f"{FMTC.TRUE}+")
            .replace("-", f"{FMTC.FALSE}-")
            .replace("]", f"{FMTC.BRACKET}]")
            .replace("#", f"{FMTC.BRACKET}[")
        )

    def _pydantic_hopefully_non_erroring_dumper(obj: PydanticBM) -> dict:
        return {k: getattr(obj, k) for k in obj.model_fields_set}

    def fmt_iterable(
        it: Iterable | Any,
        /,
        *its: Iterable | Any,
        indentation: int = 2,
        item_limit: int = 100,
        depth_limit: int = 100,
        syntax_highlighting: bool = False,
        trailing_commas: bool = True,
        int_formatter: Callable[[int], str] | None = None,
        let_no_indent: bool = True,
        force_no_indent: bool = False,
        force_no_spaces: bool = False,
        force_complex_parenthesis: bool = False,
        force_union_parenthesis: bool = True,
        prefer_full_names: bool = False,
        str_repr: Callable[[str], str] = double_quoted_repr,
        prefer_pydantic_better_dump: bool = False,
        **kwargs,
    ) -> str:
        """### Return iterable as formatted string with optional syntax highlighting.

    This also supports primitive types to be included in the iterables although passing primitive types themselves is fine.

    For printing the iterable use tcr.print_iterable().\\
    For debugging use tcr.console().

    Example:
    ```py
    >>> fmt_iterable([10, 20, 30])
    '[\\n  10,\\n  20,\\n  30,\\n]'
    >>> fmt_iterable({10: 20, 30: 40})
    '{\\n  10: 20,\\n  30: 40,\\n}'
    ```

    Args:
        it: Iterable, The iterable to format
        *its: Iterable, The same as above, if provided, it = (it, *its), can be omitted.
        indentation: int, How many spaces between where the list bracket is placed and the list items.
        item_limit: int, How many items in a list can be displayed before it's cut off. Any values < 1 will be set back to 1
        syntax_highlighting: bool, Whether or not terminal color codes should be added to make the code/iterables perttier. This also slightly changes the syntax. For example `'{,}'` with syntax highlighting and `'set()'` without. If you wish to copy & paste the iterable from terminal back to code set this to False although it may work with it set to true as well. The extra syntax safety does not support generators and `"(X more items...)"` messages that come from `item_limit`.
        trailing_commas: bool, whether or not to add trailing commas to lists (`'[\\n  10,\\n  20,\\n]'` vs `'[\\n  10,\\n  20\\n]'`). Psst: this can be set to 2 to force trailing commas although it's not recommended to use this as a feature.
        int_formatter: Callable[[int], str], A function that formats integers to a string. For example tcr.hex will format all integers as hex values. The tcr.hex formatter is automatically used unless other one was supplied
        let_no_indent: bool, Let the function automatically determine good spots to remove excessive enter-indent-syntax (for example "[\\n  10,\\n  20\\n]" - The list has only two, non iterable items or when the list has only one iterable or non iterable item)
        force_no_indent: bool, Force the condition above (let_no_spaces), skip any conditions listed there, never add extra enters or indents even if it may make the result unreadable. This effectively makes `indent` or `let_no_indent` irrelevant. This also sets `trailing_commas` to False.
        force_no_spaces: bool, Force remove any extra spaces (not including the objects' values for example strings will still be displayed with spaces). It removes spaces for example after commas, colons, etc. This effectively enables `force_no_indent` thus making `indent` or `let_no_indent` irrelevant.
        force_complex_parenthesis: bool, Force parenthesis when displaying `complex` type for example `(3 + 1j)` instead of `3+1j`. This has no effect when syntax highlighting is turned off.
        prefer_full_names: bool, whether or not to use the full names of objects if possible.
        let_no_inder_max_iterables: int = 1, (advanced) override the limit for iterables for the let_no_indent feature
        let_no_inder_max_non_iterables: int = 4, (advanced) override the limit for non-iterables for the let_no_indent feature
        str_repr: Callable[[str], str] = double_quoted_repr, (advanced) override the default string repr callable
        prefer_pydantic_better_dump: bool = False, Will use the pydantic's custom dumper which prints the model name in more places, instead of leaving it only for the moment when pydantic SHITS ITS PANTS (raises random shitass errors). i have nothing more to say about this.

    If no formatting is set for an object, it can be defined using the __tcr_display__ method.

    ```py
    class PrintableObj:
      def __tcr_display__(self=None, **kwargs) -> str:
        return 'tcr.fmt-able object' + ('\'s instance' if self is not None else '')

    >>> fmt_iterable([PrintableObj])
    'tcr.fmt-able object'
    >>> fmt_iterable([PrintableObj()])
    "tcr.fmt-able object's instance"
    ```
    """
        if depth_limit < 0:
            depth_limit = 0
        if kwargs.get("__depth", 0) > depth_limit:
            return FMT_TOO_DEEP[syntax_highlighting]

        if its:
            it = (it, *its)

        item_limit = int(item_limit)
        if item_limit < 0:
            item_limit = 1

        if (
            # if this feature is turned on:
            let_no_indent
            and not force_no_spaces
            # for all Iterables...
            and isinstance(it, Iterable)
            # ...that don't have already hardcoded displays
            and not isinstance(it, str | bytes)
            # If their length can be checked (e.g. not generators)
            and able(len, it)
            # And they have any length:
            and len(it) > 0
        ):
            if isinstance(it, Mapping):
                if len(it) == 1 and ((type(next(iter(it.values()))) in (int, float, complex, bool)) or next(iter(it.values())) in (None, Null, "", [], (), {}, set())):
                    pass  # This broke some stuff so now no mappings can be folded in
                    # force_no_indent = -1
            else:
                # Case 1: If the iterable in question contains iterables
                # If there is at most 1 iterable in the outer iterable of iterables
                if len(it) <= Or(kwargs.get("let_no_inder_max_iterables"), 1) and any(isinstance(x, Iterable) for x in it):
                    force_no_indent = -1
                # Case 2: If the outer iterable consists of non-iterables: If there are at most 4 non-iterables
                if all((not isinstance(x, Iterable)) or isinstance(x, str | bytes) or (able(len, x) and len(x) == 0) for x in it) and len(it) <= Or(
                    kwargs.get("let_no_inder_max_non_iterables"), 4
                ):
                    force_no_indent = -1

        name = "__qualname__" if prefer_full_names else "__name__"
        space = " " if not force_no_spaces else ""
        indent = space * indentation if not force_no_indent else ""
        enter = "\n" if not force_no_indent else ""
        trailing_commas = trailing_commas if (trailing_commas == 2 or not force_no_indent) else False

        if isinstance(it, Mapping) or (PydanticBM is not None and isinstance(it, PydanticBM)):
            asterisks = FMT_ASTERISK[syntax_highlighting] * 2
        elif isinstance(it, Iterable):
            asterisks = FMT_ASTERISK[syntax_highlighting] * 1
        else:
            asterisks = ""

        if int_formatter is None and isinstance(it, bytearray):
            int_formatter = tcrhex

        if force_no_indent < 0:
            force_no_indent += 1

        thisdict = {
            "indentation": indentation,
            "item_limit": item_limit,
            "syntax_highlighting": syntax_highlighting,
            "trailing_commas": trailing_commas,
            "int_formatter": int_formatter,
            "let_no_indent": let_no_indent,
            "force_no_indent": force_no_indent,
            "force_no_spaces": force_no_spaces,
            "force_complex_parenthesis": force_complex_parenthesis,
            "force_union_parenthesis": force_union_parenthesis,
            "prefer_full_names": prefer_full_names,
            "depth_limit": depth_limit,
            "prefer_pydantic_better_dump": prefer_pydantic_better_dump,
            "str_repr": str_repr,
            "no_try": kwargs.get("no_try"),
            "__depth": kwargs.get("__depth", 2) + 1,
        }
        if a := kwargs.get("let_no_inder_max_iterables"):
            thisdict["let_no_inder_max_iterables"] = a
        if a := kwargs.get("let_no_inder_max_non_iterables"):
            thisdict["let_no_inder_max_non_iterables"] = a

        this = partial(fmt_iterable, **thisdict)

        queue_name = getattr_queue(
            type(it),
            name,
            "__name__",
            "__class__.__name__",
            default=("<???>" if syntax_highlighting else "__unknown_object__"),
        )

        if hasattr(it, "__tcr_display__"):
            try:
                return it.__tcr_display__(**thisdict, _ran_from_tcr_display=True)
            except NotImplementedError:
                pass
            except Exception as e:
                if kwargs.get("_raise_errors"):
                    raise
                return FMT_INTERNAL_EXCEPTION[syntax_highlighting] % f"{queue_name}, {extract_error(e, raw=True)[0]}"

        if hasattr(it, "__tcr_fmt__"):
            try:
                tcr_formatted = it.__tcr_fmt__(**thisdict, fmt_iterable=fmt_iterable, _ran_from_tcr_display=True)

                if tcr_formatted is not None:
                    return tcr_formatted
            except NotImplementedError:
                pass
            except Exception as e:
                if kwargs.get("_raise_errors"):
                    raise
                return FMT_INTERNAL_EXCEPTION[syntax_highlighting] % f"{queue_name}, {extract_error(e, raw=True)[0]}"

        if "_force_next_type" in kwargs and kwargs.get("_ran_from_tcr_display"):
            return FMT_CLASS[syntax_highlighting] % (
                (queue_name + ("(...)" if not syntax_highlighting and not kwargs.get("_i_am_class") else "") + (FMT_LETTERS.META if syntax_highlighting and kwargs.get("_i_am_class") else "")),
                asterisks + this(it),
            )

        if isinstance(it, _OverflowClass):
            return f'{FMTC.SPECIAL}({FMTC.NUMBER}{it}{FMTC.SPECIAL} more item{"s" if it.amount != 1 else ""}...){FMTC._}' if syntax_highlighting else f"({it} more items...)"
        if isinstance(it, ....__class__):  # cursed syntax lol
            if not syntax_highlighting:
                return "..."
            return f"{FMTC.DECIMAL}..."
        if (_result := able(issubclass, it, Enum)) and (_result.result):
            return FMT_CLASS[syntax_highlighting] % (
                it.__name__ + (FMT_LETTERS.META if syntax_highlighting else ""),
                ((1 if _is_enum_auto(it) else 2) * FMT_ASTERISK[syntax_highlighting]) + this(list(it), _force_next_type=set, let_no_ident=False, _enums_next_hide_class=True),
            )

        if repr(it) == "<class 'pydantic.main.BaseModel'>":  # Kurwa pierdole tego kurwa pydantica chujowego
            return (FMTC.TYPE if syntax_highlighting else "") + "BaseModel"
        if isinstance(it, type) and hasattr(it, "__pydantic_core_schema__"):
            it_name = it.__pydantic_core_schema__

            while "schema" in it_name:
                it_name = it_name["schema"]

            it_name = it_name.get("model_name", "<UnknownPydanticType>")
            return (FMTC.TYPE if syntax_highlighting else "") + it_name
        if _HikariEnum is not None and (_result := able(issubclass, it, _HikariEnum)) and (_result.result):
            return FMT_CLASS[syntax_highlighting] % (
                it.__name__ + (FMT_LETTERS.META if syntax_highlighting else ""),
                ((1 if _is_enum_auto(it) else 2) * FMT_ASTERISK[syntax_highlighting]) + this(list(it), _force_next_type=set, let_no_ident=False, _enums_next_hide_class=True),
            )
        if isinstance(it, Enum) or (_HikariEnum is not None and isinstance(it, _HikariEnum)):
            if kwargs.get("_enums_next_hide_class"):
                if _is_enum_auto(it.__class__):
                    return FMT_ENUM_AUTO_NO_CLASS[syntax_highlighting] % it.name
                else:
                    return FMT_ENUM_NO_CLASS[syntax_highlighting] % (it.name, this(it.value, force_no_indent=True, force_complex_parenthesis=True))
            else:
                if _is_enum_auto(it.__class__):
                    return FMT_ENUM_AUTO[syntax_highlighting] % (it.__class__.__name__, it.name)
                return FMT_ENUM[syntax_highlighting] % (it.__class__.__name__, it.name, this(it.value, force_no_indent=True, force_complex_parenthesis=True))
        if PydanticBM is not None and isinstance(it, PydanticBM):
            if prefer_pydantic_better_dump:
                dumped = _pydantic_hopefully_non_erroring_dumper(it)
            else:
                try:
                    dumped = it.model_dump(warnings="none")
                except Exception:
                    # Pydantic doesn't feel like supporting sets nicely so it just errors when dumping. This just falls back to the other method and adds an exclamation mark to mark that it has errored and successfully recovered.
                    dumped = _pydantic_hopefully_non_erroring_dumper(it)

            if dumped:
                return FMT_CLASS[syntax_highlighting] % (it.__class__.__name__, asterisks + this(dumped))
            else:
                return FMT_CLASS[syntax_highlighting] % (it.__class__.__name__, "")
        if isinstance(it, dt.datetime | dt.date | dt.time):
            if isinstance(it, dt.datetime):
                format_str = "%H:%M:%S %d-%m-%Y"
            elif isinstance(it, dt.date):
                format_str = "%d-%m-%Y"
            else:
                format_str = "%H:%M:%S"

            if not syntax_highlighting:
                return repr(it)
            else:
                main_color = FMTC.NUMBER
                secondary_color = FMTC.DECIMAL
                s = f"<{it:{format_str}}>"

                for x in ("-", ":", "<", ">"):
                    s = s.replace(x, f"{secondary_color}{x}{main_color}")

                return s
        if isinstance(it, pathlib.PurePath):
            if not syntax_highlighting:
                return repr(it)

            drive, parts = it.drive, list(it.parts)

            if it.is_absolute() or parts[0] == "" or parts[0] == "\\":
                parts.pop(0)

            if drive:
                drive = f"{FMTC.DECIMAL}{drive}".replace(":", f"{FMTC.COLON}:{FMTC.DECIMAL}")

            s = f"{FMTC.SLASH}/".join(([drive] if it.is_absolute() else ([""] if it.parts[0] == "\\" else [])) + [f"{FMTC.DECIMAL}{part}" for part in parts])

            return FMT_CLASS[True] % (it.__class__.__name__, s)

        if able(issubclass, it, BaseException) and issubclass(it, BaseException):
            exc_name = extract_error(it, raw=True)[0]

            if not syntax_highlighting:
                return exc_name

            return f"{FMTC.BUILT_IN_EXCEPTION}{exc_name}"

        if not syntax_highlighting and isinstance(it, QuotelessString):
            return str(it)
        if not syntax_highlighting and isinstance(it, GayString):
            return str(it)
        if not syntax_highlighting and isinstance(it, BrainfuckCode):
            return str(it)

        if it is Null:
            return f"{FMTC.NULL}{it}{FMTC._}" if syntax_highlighting else str(it)
        if it is Undefined:
            return f"{FMTC.UNDEFINED}{it}{FMTC._}" if syntax_highlighting else str(it)
        if it is None:
            return f"{FMTC.NONE}{it}{FMTC._}" if syntax_highlighting else str(it)
        if it is True:
            return f"{FMTC.TRUE}{it}{FMTC._}" if syntax_highlighting else str(it)
        if it is False:
            return f"{FMTC.FALSE}{it}{FMTC._}" if syntax_highlighting else str(it)

        _t = kwargs.get("_force_next_type") or type(it)

        if _t == QuotelessString:
            reprit = str_repr(it)
            return f"{FMTC.STRING}{reprit[1:-1]}" if syntax_highlighting else (str_repr(it)[1:-1])
        if _t == GayString:
            return gay(it)
        if _t == BrainfuckCode:
            return _fmt_brainfuck(it)

        if _t == type:  # noqa: E721
            return f'{FMTC.TYPE}{getattr_queue(it, "__name__", "__class__.__name__", default=it)}{FMTC._}' if syntax_highlighting else str(it)

        if not kwargs.get("_force_next_type"):
            itsmro = getattr_queue(it, "__mro__", "__class__.__mro__", default=())
            # It's-a me mro

            if str in itsmro:
                _t = str  # Things displayed as ['a', 'b', 'c', 'd'] if they inherited from str
            elif bytes in itsmro:
                _t = bytes
            else:
                for item in itsmro:
                    if item in FMT_BRACKETS:
                        _t = item
                        break
        if it.__class__ == sys.version_info.__class__ and syntax_highlighting:
            return FMT_BRACKETS[tuple][1] % FMT_SYS_VERSION_INFO % it[:3]
        if _t == int:  # noqa: E721
            if int_formatter:
                it = int_formatter(it)
            return f"{FMTC.NUMBER}{it}{FMTC._}" if syntax_highlighting else str(it)
        if _t == float:  # noqa: E721
            return f'{FMTC.NUMBER}{str(it).replace(".", f"{FMTC.DECIMAL}.{FMTC.NUMBER}")}{FMTC._}' if syntax_highlighting else str(it)
        if _t == str:  # noqa: E721
            reprit = str_repr(it)
            return f"{FMTC.QUOTES}{reprit[0]}{FMTC.STRING}{reprit[1:-1]}{FMTC.QUOTES}{reprit[-1]}{FMTC._}" if syntax_highlighting else str_repr(it)
        if _t == bytes:  # noqa: E721
            reprit = repr(it)
            return f"{FMTC.BYTESTR_B}{reprit[0]}{FMTC.QUOTES}{reprit[1]}{FMTC.STRING}{reprit[2:-1]}{FMTC.QUOTES}{reprit[-1]}{FMTC._}" if syntax_highlighting else repr(it)
        if _t == complex:  # noqa: E721
            brackets = ("", "") if (not force_complex_parenthesis) else (f"{FMTC.BRACKET}(", f"{FMTC.BRACKET})")
            return (
                f"""{brackets[0]}{FMTC.NUMBER}{int(it.real) if int(it.real) == it.real else str(it.real).replace(".", f"{FMTC.DECIMAL}.{FMTC.NUMBER}")}{FMTC._}{space}{FMTC.COMPLEX}+{space}{FMTC.NUMBER}{int(it.imag) if int(it.imag) == it.imag else str(it.imag).replace(".", f"{FMTC.DECIMAL}.{FMTC.NUMBER}")}{FMTC.COMPLEX}j{brackets[1]}{FMTC._}"""
                if syntax_highlighting
                else repr(it)
            )
        if _t == UnionType:
            if force_union_parenthesis:
                return FMT_BRACKETS[tuple][syntax_highlighting] % (FMT_UNION_SEPARATOR[syntax_highlighting].join(this(x) for x in unpack_union(it)))
            else:
                return FMT_UNION_SEPARATOR[syntax_highlighting].join(this(x) for x in unpack_union(it))

        if _t == bytes_iterator:
            return FMT_ITER[syntax_highlighting] % this(bytes(it))
        if _t == str_iterator:
            return FMT_ITER[syntax_highlighting] % this("".join(it))
        if _t == bytearray_iterator:
            return FMT_ITER[syntax_highlighting] % this(bytearray(it))
        if _t == dict_keyiterator:
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=dict_keys, _ov=ov)
        if _t == dict_valueiterator:
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=dict_values, _ov=ov)
        if _t == dict_itemiterator:
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=dict_items, _ov=ov)
        if _t in (list_iterator, list_reverseiterator, zip_iterator):
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _ov=ov)
        if _t in (range_iterator, longrange_iterator):
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=range, _ov=ov)
        if _t == set_iterator:
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=set, _ov=ov)
        if _t == tuple_iterator:
            listit, ov = limited_iterable(it, item_limit)
            return FMT_ITER[syntax_highlighting] % this(listit, _force_next_type=tuple, _ov=ov)
        if _t == coroutine:
            return FMT_BRACKETS[coroutine][syntax_highlighting] % (getattr_queue(it, name, "__name__"))

        comma = f"{FMTC.COMMA}," if syntax_highlighting else ","

        is_of_prohibited_type = any(isinstance(it, x) for x in (typing._GenericAlias, typing._UnpackGenericAlias))
        # took me half an hour of debugging to discover that typing._GenericAlias contains an infinite amount of nested copies of typing._UnpackGenericAlias but only if you first iter then index not if you just index and it's a mess.

        if not is_of_prohibited_type and isinstance(it, Iterable):
            if kwargs.get("_enums_next_hide_class"):
                thisdict["_enums_next_hide_class"] = True
                this = partial(this, _enums_next_hide_class=True)

            itl, overflow = limited_iterable(it, item_limit)
            if not able(len, it) or len(it) > 0:
                if isinstance(it, Mapping):
                    inner = f"{comma}{enter or space}".join([
                        indent + (f"{k}{FMTC.COLON}:{FMTC._}{space}{v}" if syntax_highlighting else f"{k}:{space}{v}").replace("\n", f"{enter}{indent}")
                        for k, v in {this(key): this(value) for key, value in it.items()}.items()
                    ]) + (comma if trailing_commas else "")

                    return (FMT_BRACKETS[_t] if _t in FMT_BRACKETS else FMT_BRACKETS[dict])[syntax_highlighting] % f'{enter}{inner}{enter}'  # fmt: skip
                else:
                    inner = f"{comma}{enter or space}".join([
                        indent + x.replace("\n", f"\n{indent}")
                        for x in [this(element) for element in itl]
                        + ([] if not (overflow if not kwargs.get("_ov") else kwargs.get("_ov")) else [this(_OverflowClass(overflow if not kwargs.get("_ov") else kwargs.get("_ov")))])
                    ]) + (comma if (trailing_commas or (_t == tuple and len(it) == 1)) else "")  # noqa: E721

                    return (FMT_BRACKETS[_t] if _t in FMT_BRACKETS else FMT_BRACKETS[None])[syntax_highlighting] % f'{enter}{inner}{enter}'  # fmt: skip
            else:
                if _t == set and not syntax_highlighting:  # noqa: E721
                    return "set()"
                return (FMT_BRACKETS[_t] if _t in FMT_BRACKETS else FMT_BRACKETS[None])[syntax_highlighting] % (comma if _t == set else '')  # fmt: skip  # noqa: E721

        if not syntax_highlighting:
            return repr(it)

        return _fmt_unknown_highlighted(it, queue_name)
        # If no hardcoded patterns match, return a repred version of whatever it is

    globals()["fmt_iterable"] = _reset_return_wrapper(fmt_iterable)
    # Done this way to trick the IDE code snippets since the deco forwards the *args, **kwargs to the decorated func anyway...
    # If i were to @decorate the def fmt_iterable it'd replace the code snippets with the decorated function's code snippets.
    # Or i'm a dumbass and there's a better way of doing it.. (<- probably this)

    def print_iterable(
        it: Iterable,
        *its: Iterable,
        raw: bool | None = None,
        recursive: bool | None = None,
        printhook: Callable[[str], None] = print,
        **kwargs,
    ) -> None:
        """### Print iterable as formatted string with optional syntax highlighting with the given printhook.

    This also supports primitive types to be included in the iterables although passing primitive types themselves is fine.

    For formatting the iterable (and having the result returned as str) use tcr.fmt_iterable().\\
    For debugging use tcr.console().

    Example:
    ```py
    >>> print_iterable([10, 20, 30]) # Returns None, if you need str use fmt_iterable()
    [
      10,
      20,
      30,
    ]
    >>> print_iterable({10: 20, 30: 40})
    {
      10: 20,
      30: 40,
    }
    ```

    Args:
        it: Iterable, The iterable to print
        *its: Iterable, The same as above, if provided, it = (it, *its), can be omitted.
        indentation: int, How many spaces between where the list bracket is placed and the list items.
        raw: DEPRECATED, don't use. If you need raw output use fmt_iterable()
        recursive: DEPRECATED, this does not have any effect but is left for backwards-compatibility.
        printhook: Callable[[str], None], replacement for print function if provided else the built in print function
        item_limit: int, How many items in a list can be displayed before it's cut off. Any values < 1 will be set back to 1
        syntax_highlighting: bool, Whether or not terminal color codes should be added to make the code/iterables perttier. This also slightly changes the syntax. For example `'{,}'` with syntax highlighting and `'set()'` without. If you wish to copy & paste the iterable from terminal back to code set this to False although it may work with it set to true as well. The extra syntax safety does not support generators and `"(X more items...)"` messages that come from `item_limit`.
        trailing_commas: bool, whether or not to add trailing commas to lists (`'[\\n  10,\\n  20,\\n]'` vs `'[\\n  10,\\n  20\\n]'`)
        int_formatter: Callable[[int], str]: A function that formats integers to a string. For example tcr.hex will format all integers as hex values. The tcr.hex formatter is automatically used unless other one was supplied
        let_no_indent: bool, Let the function automatically determine good spots to remove excessive enter-indent-syntax (for example "[\\n  10,\\n  20\\n]" - The list has only two, non iterable items or when the list has only one iterable or non iterable item)
        force_no_indent: bool, Force the condition above (let_no_spaces), skip any conditions listed there, never add extra enters or indents even if it may make the result unreadable. This effectively makes `indent` or `let_no_indent` irrelevant. This also sets `trailing_commas` to False.
        force_no_spaces: bool, Force remove any extra spaces (not including the objects' values for example strings will still be displayed with spaces). It removes spaces for example after commas, colons, etc. This effectively enables `force_no_indent` thus making `indent` or `let_no_indent` irrelevant.
        force_complex_parenthesis: bool, Force parenthesis when displaying `complex` type for example `(3 + 1j)` instead of `3+1j`. This has no effect when syntax highlighting is turned off.
        prefer_full_names: bool, whether or not to use the full names of objects if possible.
        str_repr: Callable[[str], str] = double_quoted_repr, (advanced) override the default string repr callable
        **kwargs: Anything from there is passed in into the fmt_iterable call
    """
        result = fmt_iterable(it, *its, **kwargs)
        if recursive is not None:
            warn(
                "`recursive` is deprecated. It's always set to True in new print_iterable()",
                DeprecationWarning,
                stacklevel=2,
            )
        if raw:
            warn(
                "`raw` is deprecated. Use fmt_iterable() instead",
                DeprecationWarning,
                stacklevel=2,
            )
            return result
        printhook(result)


def alert(s: str, *, printhook: Callable[[str], None] = print, raw=False) -> None:
    text = "".join([f"{(Fore.BLACK + Back.RED + Style.bold) if i % 2 == 0 else Fore.BLACK + Back.YELLOW}{x}" for i, x in enumerate(s)]) + Style.reset

    if raw:
        return text

    printhook(text)


def gay(text: str, offset: int = 0) -> str:
    """Turn a string gay. Happy pride :3"""  # noqa: D400
    colors = [Fore.RED, Fore.orange_1, Fore.YELLOW, Fore.GREEN, Fore.MAGENTA, Fore.BLUE, Fore.purple_1b, Fore.purple_4b]

    if text != "tcrutils":
        colors.pop()

    colors = colors + colors[1:-1:-1]

    result = ""

    for i, char in enumerate(text):
        color = colors[(i - offset) % len(colors)]
        result += color + Style.bold + char

    result += FMTC._
    return result
