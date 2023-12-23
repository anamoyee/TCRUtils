def dir2(x: object, /) -> list[str]:
  return [y for y in dir(x) if not y.startswith('__')]


def dir3(x: object, /) -> list[str]:
  return [y for y in dir(x) if not y.startswith('_')]
