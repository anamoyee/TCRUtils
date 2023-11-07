import re as regex
from collections.abc import Callable, Iterable
from typing import Literal

from .tcr_regex import URL_PATTERN


def batched(it: str | Iterable, n: int) -> list:
  """### Poor man's (Py3.11) itertools.batched().

  Returns a list of splits of the original `it` Iterable that was passed in, split every `n` items. Last group may be smaller than `n` items if the source was exhausted
  """
  return [it[i : i + n] for i in range(0, len(it), n)]


def cut_at(
  it: str | Iterable,
  n: int,
  end: str | Iterable = '...',
  *,
  filter_links: Literal[False] | str | Callable = False,
) -> str:
  """### Return a cut off part of the provided `it` iterable.

  with the `end` added at the end such that the return value is exactly `n` in length.\\
  Mainly strings but also supports other iterables\\
  Set `end` to `''`/`[]` to disable it.\\

  Use `filter_links` to shorten links to this string, only applicable if the iterable provided is a string and if the iterable exceeded `n`, else nothing will be affected
  - `$1` - Entire link
  - `$2` - http/https (will keep the 's' if present, that's its point)
  - `$3` - any `subdomains.` (if present), `.domains.` or `.tld`s
  - `$4` - `.domain` (second to last (possibly after . and) before the last .)
  - `$5` - `.tld` (in between the last . and / or end of match)
  - `$6` - part of the link after `/` (not including it, may be '')

  https://regex101.com/r/46LZtS/1
  """
  if len(it) <= n:
    return it
  if filter_links is not False and isinstance(it, str):
    if not isinstance(filter_links, str | Callable):
      msg = f'Set filter_links to a str of the replacement value for links or Callable, not {filter_links!r}'
      raise ValueError(msg)
    it = regex.sub(URL_PATTERN, filter_links, it)
    if len(it) <= n:
      return it
  if n > len(end):
    return it[: (n - len(end))] + end
  if n > 0:
    return end[:n]
  return ''
