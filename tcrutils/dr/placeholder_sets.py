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
  # Author
  'username':      __.username,
  'user_name':     __.username,
  'user name':     __.username,
  'globalname':    __.globalname,
  'global_name':   __.globalname,
  'global name':   __.globalname,
  'nickname':      __.nickname,
  'nick_name':     __.nickname,
  'nick name':     __.nickname,
  'mention':       __.mention,
  '@':             __.mention,
  '@@':  __partial(__.mention, 'noping'),
  'discriminator': __.discriminator,
  'discrim':       __.discriminator,
  'tag':           __.tag,
  'id':            __.id,
  'bot':           __.bot,
  'isbot':         __.bot,
  'human':         __.human,
  'ishuman':       __.human,
  'roles':         __.roles,
  'avatar':        __.avatar,
  'color':         __.color,
  'rolecolor':     __.color,

  # Server
  'server':        __.server,

  # Misc
  'indms':         __.in_dms,
  'in_dms':        __.in_dms,
  'in dms':        __.in_dms,
}
"""Ctrl+click whatever you're hovering on to see aliases for all the discord placeholders."""

DISCORD_TROUBLEMAKERS = {
  'attach':     __.attach,
  'attachment': __.attach, # May cause a BadRequestError when a technically valid link is supplied but one that doesn't point to any valid file to attach.
}

ALL_DISCORD = {**DISCORD, **DISCORD_TROUBLEMAKERS}

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
"""WARNING: Unsafe math operations are those which may stall the main python thread forever if certain arguments are supplied.

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

# fmt: on

SAFE_AND_UNSAFE_MATH = {**UNSAFE_MATH, **SAFE_MATH}
"""WARNING: This contains both UNSAFE and safe sides of the math module. To see more see .UNSAFE_MATH docstring.

Ctrl+click whatever you're hovering on to see aliases for all the math placeholders.
"""

ALL = merge_dicts(
  *[y for x, y in vars().items() if x.upper() == x and x.lower() != x],
  # {x: y for x, y in vars(__).items() if not x.startswith('_') and not x.startswith('p_')},
)
ALL_NON_DISCORD = {x: y for x, y in ALL.items() if x not in ALL_DISCORD}
ALL_NON_UNSAFEMATH = {x: y for x, y in ALL.items() if x not in UNSAFE_MATH}
ALL_NON_UNSAFEMATH_NON_DISCORD = {x: y for x, y in ALL.items() if x not in UNSAFE_MATH and x not in ALL_DISCORD}
