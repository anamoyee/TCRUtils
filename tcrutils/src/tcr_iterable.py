import re as regex
from collections.abc import Callable, Iterable
from typing import Literal

from .tcr_regex import Regex, RegexPreset


def batched(
  it: str | Iterable,
  n: int,
  *,
  back_to_front: bool = False,
) -> list:
  """### Poor man's `itertools.batched()` (on Py3.11).

  Returns a list of splits of the original `it` Iterable that was passed in, split every `n` items. Last group may be smaller than `n` items if the source was exhausted
  `back_to_front`: makes the items pile up in the back and now the first item is the one to have less than n items if there's not enough to pack it with. For example:
  - `batched("1234567890", n=3)                    ` returns `["123", "456", "789", "0"]`
  - `batched("1234567890", n=3, back_to_front=True)` returns `["1", "234", "567", "890"]`
  """
  if back_to_front:
    return [x[::-1] for x in batched(it[::-1], n=n, back_to_front=False)[::-1]]
  return [it[i : i + n] for i in range(0, len(it), n)]


def cut_at(
  it: str | Iterable,
  n: int,
  end: str | Iterable = '...',
  *,
  filter_links: Literal[False] | str | Callable = False,
  shrink_links_visually_if_fits: bool = False,
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

  `shrink_links_visually_if_fits` replaces links with their markdown counterparts where the visible text is http(s):/subdomain.domain.tld/ (no further part of the links is visible, but the entire link is contained)
  """
  if len(it) <= n:
    if (
      shrink_links_visually_if_fits
      and len(a := regex.sub(RegexPreset.URL, r'[\2:/\3/](<\1>)', it)) <= n
    ):  # :/ instead of :// because discord bruh
      return a
    return it
  if filter_links is not False and isinstance(it, str):
    if not isinstance(filter_links, str | Callable):
      msg = f'Set filter_links to a str of the replacement value for links or Callable, not {filter_links!r}'
      raise ValueError(msg)
    it = regex.sub(RegexPreset.URL, filter_links, it)
    if len(it) <= n:
      return it
  if n > len(end):
    return it[: (n - len(end))] + end
  if n > 0:
    return end[:n]
  return ''
