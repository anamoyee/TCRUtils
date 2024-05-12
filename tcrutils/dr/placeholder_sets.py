"""TODO: Make a markdown doc of all the placeholders sorted by sets like robotop dynamic response page."""

from functools import partial as __partial

from ..src.tcr_console import console as c
from ..src.tcr_dict import merge_dicts
from . import placeholders as __

# fmt: off

TEXT = {
  'comment': __.comment,
  '#':       __.comment,
  '//':      __.comment,
  'var':     __.var,
}
"""Ctrl+click whatever you're hovering on to see aliases for all the text placeholders"""

DISCORD = {
  'username': __.username,
  'mention':  __.mention,
  '@':        __.mention,
  '@@':       __partial(__.mention, 'noping'),
}
"""Ctrl+click whatever you're hovering on to see aliases for all the discord placeholders."""

UNSAFE_MATH = {
  'add':         __.add,
  'subtract':    __.subtract,
  'sub':         __.subtract,
  'multiply':    __.multiply,
  'mul':         __.multiply,
  'divide':      __.divide,
  'div':         __.divide,
  'floordivide': __.floordivide,
  'fdiv':        __.floordivide,
  'floordiv':    __.floordivide,
  'power':       __.power,
  'pow':         __.power,
  'modulo':      __.modulo,
  'mod':         __.modulo,
}
"""Unsafe math operations are those which may stall the main python thread forever if certain arguments are supplied.

I tried searching far and wide for a time-based termination solution but i couldn't find any that worked or worked not only on unix.

Ctrl+click whatever you're hovering on to see aliases for all the unsafe math placeholders.
"""

SAFE_MATH = {
  'round':   __.round_,
  'floor':   __.floor,
  'ceil':    __.ceil,
  'ceiling': __.ceil,
}
"""Read unsafe math operations doc string to find out what are safe ones.

Ctrl+click whatever you're hovering on to see aliases for all the safe math placeholders.
"""

MATH = {**UNSAFE_MATH, **SAFE_MATH}
"""WARNING: This contains both UNSAFE and safe sides of the math module. To see more see .UNSAFE_MATH docstring.

Ctrl+click whatever you're hovering on to see aliases for all the math placeholders.
"""

# fmt: on

ALL = merge_dicts(
  *[y for x, y in vars().items() if x.upper() == x and x.lower() != x],
  {x: y for x, y in vars(__).items() if not x.startswith('_') and not x.startswith('p_')},
)
ALL_NON_DISCORD = {x: y for x, y in ALL.items() if x not in DISCORD}
ALL_NON_UNSAFEMATH = {x: y for x, y in ALL.items() if x not in UNSAFE_MATH}
ALL_NON_UNSAFEMATH_NON_DISCORD = {x: y for x, y in ALL.items() if x not in UNSAFE_MATH and x not in DISCORD}
