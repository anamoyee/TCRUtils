from collections.abc import (
  Callable,
  Generator,
  ItemsView,
  Iterable,
  KeysView,
  Mapping,
  ValuesView,
)
from functools import cache, partial, wraps
from types import GeneratorType
from typing import TypeAlias
from warnings import warn

from colored import attr, fg

from .tcr_color import c
from .tcr_compare import able
from .tcr_constants import NEWLINE
from .tcr_int import hex as tcrhex
from .tcr_null import Null

PIRepassable: TypeAlias = (
  type(Null)
  | list
  | tuple
  | dict
  | set
  | Generator
  | range
  | bytes
  | bytearray
  | str
  | None
  | bool
  | int
  | float
)

# fmt: off
BRACKET_COLOR    = "Cyan"

COLON_COLOR      = "Orange\\_1"
COMMA_COLOR      = "Dark\\_gray"

B_COLOR          = "Red" # b''

TRUE_COLOR       = "Green"
FALSE_COLOR      = "Red"

NULL_COLOR       = "Dark\\_gray"
NONE_COLOR       = "Light\\_gray"

MORE_ITEMS_COLOR = "Purple\\_1B"
# fmt: on


def print_block(
  text: str,
  border_char: str = '#',
  *,
  margin: int = 1,
  border: int = 3,
  padding: int = 0,
  padding_top: int = 1,
  padding_bottom: int = 1,
  text_color: str = 'Gold',
  border_color: str = 'White',
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
    msg = f'Invalid margin, border and/or padding(s) configuration {(margin, border, padding, padding_top, padding_bottom)!r}. Override this by passing in allow_invalid_config=True'
    raise ValueError(msg)

  if not allow_invalid_config and len(border_char) != 1:
    msg = f'border_char must be 1 character long (got {border_char!r} which is {len(border_char)!r} characters long). Override this by passing in allow_invalid_config=True'
    raise ValueError(msg)

  if text_color != '':
    text_color = c(text_color)
  if border_color != '':
    border_color = c(border_color)
  reset = c('reset')

  if not text_color and not border_color:
    reset = ''

  bar = f'{border_char * (border + margin + len(text) + margin + border)}'
  block = f"""
{padding_top * NEWLINE}{padding * ' '}{reset}{border_color}{bar}
{padding * ' '}{border * border_char}{reset}{margin * ' '}{text_color}{text}{reset}{margin * ' '}{border_color}{border * border_char}
{padding * ' '}{bar}{reset}{padding_bottom * NEWLINE}
"""[1:-1]
  if raw:
    return block

  print(block)
  return None


if True:  # \/ # fmt & print iterable
  # fmt: off
  class _F:
    _          = attr(0) # Reset
    NUMBER     = fg('blue')       + attr('bold')
    DECIMAL    = fg('white')      + attr('bold')
    BRACKET    = fg('cyan')       + attr('bold')
    STRING     = attr(0)          + fg('yellow')
    QUOTES     = fg('white')      + attr('bold')
    COLON      = fg('orange_1')   + attr('bold')
    COMPLEX    = fg('orange_1')   + attr('bold')
    COMMA      = fg('dark_gray')  + attr('bold')
    BYTESTR_B  = fg('red')        + attr('bold')
    TRUE       = fg('green')      + attr('bold')
    FALSE      = fg('red')        + attr('bold')
    NULL       = fg('dark_gray')  + attr('bold')
    NONE       = fg('light_gray') + attr('bold')
    MORE_ITEMS = fg('purple_1B')  + attr('bold')

  _F_BRACKETS: dict[type | None, tuple[str, str]] = { # Format Brackets
    None:              ('[%s]', f'{_F.BRACKET}[{_F._}%s{_F.BRACKET}]{_F._}'),
    list:              ('[%s]', f'{_F.BRACKET}[{_F._}%s{_F.BRACKET}]{_F._}'),
    type({}.keys()):   ('[%s]', f'{_F.MORE_ITEMS}K{_F.BRACKET}[{_F._}%s{_F.BRACKET}]{_F._}'),
    type({}.values()): ('[%s]', f'{_F.MORE_ITEMS}V{_F.BRACKET}[{_F._}%s{_F.BRACKET}]{_F._}'),
    type({}.items()):  ('[%s]', f'{_F.MORE_ITEMS}I{_F.BRACKET}[{_F._}%s{_F.BRACKET}]{_F._}'),
    set:               ('{%s}', f'{_F.BRACKET}{{{_F._}%s{_F.BRACKET}}}{_F._}'),
    frozenset:         ('frozenset({%s})', f'{_F.MORE_ITEMS}F{_F.BRACKET}{{{_F._}%s{_F.BRACKET}}}{_F._}'),
    dict:              ('{%s}', f'{_F.BRACKET}{{{_F._}%s{_F.BRACKET}}}{_F._}'),
    tuple:             ('(%s)', f'{_F.BRACKET}({_F._}%s{_F.BRACKET}){_F._}'),
    GeneratorType:     ('((%s))', f'{_F.BRACKET}<{_F._}%s{_F.BRACKET}>{_F._}'),
    range:             ('((%s))', f'{_F.BRACKET}<{_F._}%s{_F.BRACKET}>{_F._}'),
    bytearray:         ('bytearray([%s])', f'{_F.BYTESTR_B}b{_F.BRACKET}[{_F._}%s{_F.BRACKET}]{_F._}'),
  }
  # fmt: on

  def _limited_iterator(it: Iterable, limit: int) -> tuple[Iterable, int]:
    list_ = []
    for i, item in enumerate(it):
      list_.append(item)
      if i + 2 > limit:
        overflow = len(it) - limit if able(len, it) else -1
        return list_, overflow
    return list_, 0

  class _OverflowClass:
    amount: int

    def __init__(self, amount) -> None:
      self.amount = amount

    def __str__(self) -> str:
      return str(self.amount) if self.amount != -1 else '?'

  def _reset_return_wrapper(func):
    @wraps(func)
    def wrapper(*args, append_syntax_reset: bool = True, **kwargs):
      if kwargs.get('syntax_highlighting') and append_syntax_reset:
        return f'{_F._}{func(*args, **kwargs)}{_F._}'
      return func(*args, **kwargs)

    return wrapper

  def fmt_iterable(
    it: Iterable,
    /,
    *its: Iterable,
    indentation: int = 2,
    item_limit: int = 100,
    syntax_highlighting: bool = False,
    trailing_commas: bool = True,
    int_formatter: Callable[[int], str] | None = None,
    let_no_indent: bool = True,
    force_no_indent: bool = False,
    force_no_spaces: bool = False,
    force_complex_parenthesis: bool = False,
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
    """
    if its:
      it = (it, *its)

    item_limit = int(item_limit)
    if item_limit < 1:
      item_limit = 1

    if (
      # if this feature is turned on:
      let_no_indent and not force_no_spaces
      # for all Iterables...
      and isinstance(it, Iterable)
      # ...that don't have already hardcoded displays or mapping because mapping
      and not isinstance(it, str | bytes | Mapping)
      # If their length can be checked (e.g. not generators)
      and able(len, it)
      # And they have any length:
      and len(it) > 0
    ):
      # Case 1: If the iterable in question contains iterables
      # If there is at most 1 iterable in the outer iterable of iterables
      if len(it) <= 1 and isinstance(it[0], Iterable):
        force_no_indent = -1
      # Case 2: If the outer iterable consists of non-iterables: If there are at most 4 non-iterables
      if all((not isinstance(x, Iterable)) or isinstance(x, str | bytes) or (able(len, x) and len(x) == 0) for x in it) and len(it) <= 5:
        force_no_indent = -1

    space = ' ' if not force_no_spaces else ''
    indent = space * indentation if not force_no_indent else ''
    enter = '\n' if not force_no_indent else ''
    trailing_commas = trailing_commas if (trailing_commas == 2 or not force_no_indent) else False

    if int_formatter is None and isinstance(it, bytearray):
      int_formatter = tcrhex

    if force_no_indent < 0: force_no_indent += 1

    this = partial(
      fmt_iterable,
      indentation=indentation,
      item_limit=item_limit,
      syntax_highlighting=syntax_highlighting,
      trailing_commas=trailing_commas,
      int_formatter=int_formatter,
      let_no_indent=let_no_indent,
      force_no_indent=force_no_indent,
      force_no_spaces=force_no_spaces,
      force_complex_parenthesis=force_complex_parenthesis,
    )

    if isinstance(it, _OverflowClass):
      return (
        f'{_F.MORE_ITEMS}({_F.NUMBER}{it}{_F.MORE_ITEMS} more items...){_F._}'
        if syntax_highlighting
        else f'({it} more items...)'
      )
    if it is Null:
      return f'{_F.NULL}{it}{_F._}' if syntax_highlighting else str(it)
    if it is None:
      return f'{_F.NONE}{it}{_F._}' if syntax_highlighting else str(it)
    if it is True:
      return f'{_F.TRUE}{it}{_F._}' if syntax_highlighting else str(it)
    if it is False:
      return f'{_F.FALSE}{it}{_F._}' if syntax_highlighting else str(it)

    _t = type(it)

    if _t == int:
      if int_formatter:
        it = int_formatter(it)
      return f'{_F.NUMBER}{it}{_F._}' if syntax_highlighting else str(it)
    if _t == float:
      return (
        f'{_F.NUMBER}{str(it).replace(".", f"{_F.DECIMAL}.{_F.NUMBER}")}{_F._}'
        if syntax_highlighting
        else str(it)
      )
    if _t == str:
      reprit = repr(it)
      return (
        f'{_F.QUOTES}{reprit[0]}{_F.STRING}{reprit[1:-1]}{_F.QUOTES}{reprit[-1]}{_F._}'
        if syntax_highlighting
        else repr(it)
      )
    if _t == bytes:
      reprit = repr(it)
      return (
        f'{_F.BYTESTR_B}{reprit[0]}{_F.QUOTES}{reprit[1]}{_F.STRING}{reprit[2:-1]}{_F.QUOTES}{reprit[-1]}{_F._}'
        if syntax_highlighting
        else repr(it)
      )
    if _t == complex:
      brackets = (
        ('', '') if (not force_complex_parenthesis) else (f'{_F.BRACKET}(', f'{_F.BRACKET})')
      )
      return (
        f"""{brackets[0]}{_F.NUMBER}{int(it.real) if int(it.real) == it.real else str(it.real).replace(".", f"{_F.DECIMAL}.{_F.NUMBER}")}{_F._}{space}{_F.COMPLEX}+{space}{_F.NUMBER}{int(it.imag) if int(it.imag) == it.imag else str(it.imag).replace(".", f"{_F.DECIMAL}.{_F.NUMBER}")}{_F.COMPLEX}j{brackets[1]}{_F._}"""
        if syntax_highlighting
        else repr(it)
      )

    comma = f'{_F.COMMA},' if syntax_highlighting else ','
    if isinstance(it, Iterable):
      itl, overflow = _limited_iterator(it, item_limit)
      if not able(len, it) or len(it) > 0:
        if isinstance(it, Mapping):
          inner = f'{comma}{enter or space}'.join(
            [
              indent
              + (
                f'{k}{_F.COLON}:{_F._}{space}{v}' if syntax_highlighting else f'{k}:{space}{v}'
              ).replace('\n', f'{enter}{indent}')
              for k, v in {this(key): this(value) for key, value in it.items()}.items()
            ]
          ) + (comma if trailing_commas else '')

          return (_F_BRACKETS[_t] if _t in _F_BRACKETS else _F_BRACKETS[None])[syntax_highlighting] % f'{enter}{inner}{enter}'  # fmt: skip
        else:
          inner = f'{comma}{enter or space}'.join(
            [
              indent + x.replace('\n', f'\n{indent}')
              for x in [this(element) for element in itl]
              + ([] if not overflow else [this(_OverflowClass(overflow))])
            ]
          ) + (comma if (trailing_commas or (isinstance(it, tuple) and len(it) == 1)) else '')

          return (_F_BRACKETS[_t] if _t in _F_BRACKETS else _F_BRACKETS[None])[syntax_highlighting] % f'{enter}{inner}{enter}'  # fmt: skip
      else:
        if _t == set and not syntax_highlighting:
          return 'set()'
        return (_F_BRACKETS[_t] if _t in _F_BRACKETS else _F_BRACKETS[None])[syntax_highlighting] % (comma if _t == set else '')  # fmt: skip

    return str(it)

  globals()['fmt_iterable'] = _reset_return_wrapper(fmt_iterable)

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
        '`raw` is deprecated. Use fmt_iterable() instead',
        DeprecationWarning,
        stacklevel=2,
      )
      return result
    printhook(result)
