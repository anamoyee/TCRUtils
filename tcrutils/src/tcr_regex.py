from collections.abc import Iterable
from functools import partial
from re import Match


def _escaper(groups: Iterable[int], match: Match):
	s = ""
	for groupint in groups:
		group = match.group(abs(groupint))
		if groupint < 0:
			group = (type(group), repr(group))
		s += group


handler = partial(_escaper, [1, -2, 3, 4])


class RegexPreset:
	"""Provies documented preset regex patterns."""

	URL = r"((https?):\/\/((?:\S+\.)?([^\/\s]+)?\.([^\/\s]+))\/?(\S+)?)"
	"""Matches any http/https URL

  use `URL.replace('https?', 'your_protocol')` to assert different protocol.

  Groups:
      - `$1` - Entire link
      - `$2` - http/https (will keep the 's' if present, that's its point, or custom protocol if set with instruction above)
      - `$3` - any `subdomains.` (if present), `.domains.` or `.tld`s
      - `$4` - `.domain` (second to last (possibly after . and) before the last .)
      - `$5` - `.tld` (in between the last . and / or end of match)
      - `$6` - part of the link after `/` (not including it, may be `''`)

  https://regex101.com/r/46LZtS/1
  """

	MARKDOWN_HEADING = (r"(^|\n)#{1,3}\s(.|\n|\Z)(.*)", partial(_escaper, [1, -2, 3, 4]))
	"""Used when wanting to remove discord heading markdown from a string. re.sub(*MARKDOWN_HEADING, to_replace)"""


__all__ = ["RegexPreset"]
