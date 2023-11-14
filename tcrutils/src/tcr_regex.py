class RegexPreset:
  """Provies documented preset regex patterns."""

  URL = r'((https?):\/\/((?:\S+\.)?([^\/\s]+)?\.([^\/\s]+))\/?(\S+)?)'
  """Matches any URL

  Groups:
      - `$1` - Entire link
      - `$2` - http/https (will keep the 's' if present, that's its point)
      - `$3` - any `subdomains.` (if present), `.domains.` or `.tld`s
      - `$4` - `.domain` (second to last (possibly after . and) before the last .)
      - `$5` - `.tld` (in between the last . and / or end of match)
      - `$6` - part of the link after `/` (not including it, may be `''`)

  https://regex101.com/r/46LZtS/1
  """


__all__ = ['RegexPreset']
