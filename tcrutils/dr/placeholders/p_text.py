from .. import util as __


@__.REQUIRE('__vars')
def var(_, name: str, value: str | None = None, *args, __vars: dict[str, str], **kwargs):
  """### Simple, single-scope variables.

  Two modes:
   - Set: `{var|key|value}`
   - Get: `{var|key}` OR `{key}`

  You first have to set a value to something - if it doesn't exist `''` (an empty string) is returned.

  Example:
  ```txt
  {var|var1|nya}{var1} {var|var1}
  ```

  Result:
  ```txt
  nya nya
  ```
  """
  if value is not None:
    __vars[name] = value
  else:
    return __vars.get(name, '')


@__.REQUIRE_POSITIONAL(2, None)
def test(_, left: str, right: str, iftrue: str = 'true', iffalse: str = 'false', **ctxs) -> str:
  """### =IF() from excel. Returns the third parameter if the first two are equal otherwise the fourth.

  If less than 2 parameters are passed, the placeholder is left uneavaluated (stays as a string of '{test|arg1})

  Example:
  ```txt
  {test| {username} | Colon | Your username is Colon! | Your username is not Colon!}
  ```

  Result:
  ```txt
  Your username is not Colon!
  (but if Colon ran this command, it would give the other response!)
  ```
  """
  if left == right:
    return iftrue
  else:
    return iffalse


def comment(*args, **ctxs) -> str:
  """### Return empty string no matter the arguments/contexts.

  Example:
  ```txt
  {#|this is a comment}This is te{#|another comment}xt
  ```

  Result:
  ```txt
  This is text
  ```
  """


__all__ = [x for x in globals() if not x.startswith('_')]
