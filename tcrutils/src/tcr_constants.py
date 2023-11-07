# fmt: off
BACKSLASH  = '\\'
NEWLINE    = '\n'
BACKTICK   = '`'
APOSTROPHE = "'"
QUOTE      = '"'
FAKE_PIPE  = '¦'

__all__ = [x for x in globals().copy() if not x.startswith('_')]
