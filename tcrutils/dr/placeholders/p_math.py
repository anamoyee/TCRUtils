from .. import util as __


@__.STRINGIFY
@__.FLATTEN_IF_POSSIBLE
def add(_, *args: str, **ctxs) -> int | float:
  """### Add numbers (supports any number of args).

  Example:
  ```txt
  {add|1|2|3}
  ```

  Result:
  ```txt
  6
  ```
  """
  args = [__.number(x, flatten_to_int_when_possible=True) for x in args]
  return sum(args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, 0)
@__.FLATTEN_IF_POSSIBLE
def subtract(_, *args: str, **ctxs) -> int | float:
  """### Subtract numbers (supports any number of args).

  Example:
  ```txt
  {add|1|2|3}{#|evaluates to putting a '-' between each number: 1 - 2 - 3}
  ```

  Result:
  ```txt
  -4
  ```
  """
  args = [__.number(x, flatten_to_int_when_possible=True) for x in args]

  if len(args) < 2:
    return args[0]

  return __.functools.reduce(lambda x, y: x - y, args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, 1)
@__.FLATTEN_IF_POSSIBLE
def multiply(_, *args: str, **ctxs) -> int | float:
  """### Multiply numbers (supports any number of args).

  Example:
  ```txt
  {multiply|2|2|3}
  ```

  Result:
  ```txt
  12
  ```
  """
  args = [__.number(x, flatten_to_int_when_possible=True) for x in args]

  if len(args) < 2:
    return args[0]

  return __.functools.reduce(lambda x, y: x * y, args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, 1)
@__.FLATTEN_IF_POSSIBLE
def divide(_, *args: str, **ctxs) -> int | float:
  """### Divide numbers (supports any number of args).

  Example:
  ```txt
  {divide|1|2}{#|in case of >2 arguments evaluates to putting a '/' between each number: 1 / 2 / 3}
  ```

  Result:
  ```txt
  0.5
  ```
  """
  args = [__.number(x, flatten_to_int_when_possible=True) for x in args]

  if len(args) < 2:
    return args[0]

  return __.functools.reduce(lambda x, y: x / y, args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, 1)
@__.FLATTEN_IF_POSSIBLE
def floordivide(_, *args: str, **ctxs) -> int | float:
  """### Floor divide numbers (supports any number of args).

  Example:
  ```txt
  {floordivide|34|3}{#|in case of >2 arguments evaluates to putting a '//' between each number: 1 // 2 // 3}
  ```

  Result:
  ```txt
  11
  ```
  """
  args = [__.number(x, flatten_to_int_when_possible=True) for x in args]

  if len(args) < 2:
    return int(args[0])

  return __.functools.reduce(lambda x, y: x // y, args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, None)
@__.FLATTEN_IF_POSSIBLE
def power(_, base: str, exponent: str = '2', *args: str, **ctxs) -> int | float:
  args = [__.number(x, flatten_to_int_when_possible=True) for x in (base, exponent, *args)]

  return __.functools.reduce(lambda x, y: x**y, args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, None)
@__.FLATTEN_IF_POSSIBLE
def modulo(_, *args: str, **ctxs) -> int | float:
  """### Modulo numbers (supports any number of args).

  Example:
  ```txt
  {modulo|34|3}{#|in case of >2 arguments evaluates to putting a '%' between each number: 1 % 2 % 3}
  ```

  Result:
  ```txt
  1
  ```
  """
  args = [__.number(x, flatten_to_int_when_possible=True) for x in args]

  if len(args) < 2:
    return args[0]

  return __.functools.reduce(lambda x, y: x % y, args)


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, None)
def round_(_, n: str, *args: str, **ctxs) -> int | float:
  """### Round numbers using python's round function. (This DISCARDS any extra arguments!).

  This does not just round halves up, see: https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even

  Example:
  ```txt
  {round|1.2}
  {round|1.5}
  {round|2.5}
  {round|3.5}
  {round|4.5}
  ```

  Result:
  ```txt
  1
  2
  2
  4
  4
  ```
  """
  return round(__.number(n))


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, None)
def floor(_, n: str, *args: str, **ctxs) -> int | float:
  """### Round down. (This DISCARDS any extra arguments!).

  Example:
  ```txt
  {floor|6.1}
  {floor|6.9}
  ```

  Result:
  ```txt
  6
  6
  ```
  """
  return __.math.floor(__.number(n))


@__.STRINGIFY
@__.REQUIRE_POSITIONAL(1, None)
def ceil(_, n: str, *args: str, **ctxs) -> int | float:
  """### Round up. (This DISCARDS any extra arguments!).

  Example:
  ```txt
  {ceil|9.1}
  {ceil|9.9}
  ```

  Result:
  ```txt
  10
  10
  ```
  """
  return __.math.ceil(__.number(n))
