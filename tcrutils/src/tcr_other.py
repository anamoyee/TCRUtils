"""`other` submodule contains things that did not deserve their own files."""


def intbool(x: object, /):
  """Return int(bool(x)). Kept for backwards-compatibility reasons. Idk why i even made this function but i'm too scared of something not working to remove it."""
  return int(bool(x))
