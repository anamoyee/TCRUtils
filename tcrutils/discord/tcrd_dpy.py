"""### This code was not written by me, however it's licensed with the MIT License which allows for free copy and sublicensing of the licensed material.

Also i ain't depending on a whole ass package just for markdown escaping.

This code was copied from the [discord.py](https://github.com/Rapptz/discord.py) python package.

Copy of the original license (applies only to this file):

```txt
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
```

Small modifications were made to this code
"""

import re

_MARKDOWN_ESCAPE_SUBREGEX = '|'.join(r'\{0}(?=([\s\S]*((?<!\{0})\{0})))'.format(c) for c in ('*', '`', '_', '~', '|'))  # noqa: UP032
_MARKDOWN_ESCAPE_COMMON = r'^>(?:>>)?\s|\[.+\]\(.+\)'
_MARKDOWN_ESCAPE_REGEX = re.compile(rf'(?P<markdown>{_MARKDOWN_ESCAPE_SUBREGEX}|{_MARKDOWN_ESCAPE_COMMON})', re.MULTILINE)
_URL_REGEX = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'
_MARKDOWN_STOCK_REGEX = rf'(?P<markdown>[_\\~|\*`#-]|{_MARKDOWN_ESCAPE_COMMON})'


def remove_markdown(text: str, *, ignore_links: bool = True) -> str:
  """A helper function that removes markdown characters.

  .. versionadded:: 1.7

  .. note::
          This function is not markdown aware and may remove meaning from the original text. For example,
          if the input contains ``10 * 5`` then it will be converted into ``10  5``.

  Parameters
  -----------
  text: :class:`str`
      The text to remove markdown from.
  ignore_links: :class:`bool`
      Whether to leave links alone when removing markdown. For example,
      if a URL in the text contains characters such as ``_`` then it will
      be left alone. Defaults to ``True``.

  Returns
  --------
  :class:`str`
      The text with the markdown special characters removed.
  """

  def replacement(match):
    groupdict = match.groupdict()
    return groupdict.get('url', '')

  regex = _MARKDOWN_STOCK_REGEX
  if ignore_links:
    regex = f'(?:{_URL_REGEX}|{regex})'
  return re.sub(regex, replacement, text, count=0, flags=re.MULTILINE)


def escape_markdown(text: str, *, as_needed: bool = False, ignore_links: bool = True) -> str:
  r"""A helper function that escapes Discord's markdown.

  Parameters
  -----------
  text: :class:`str`
      The text to escape markdown from.
  as_needed: :class:`bool`
      Whether to escape the markdown characters as needed. This
      means that it does not escape extraneous characters if it's
      not necessary, e.g. ``**hello**`` is escaped into ``\*\*hello**``
      instead of ``\*\*hello\*\*``. Note however that this can open
      you up to some clever syntax abuse. Defaults to ``False``.
  ignore_links: :class:`bool`
      Whether to leave links alone when escaping markdown. For example,
      if a URL in the text contains characters such as ``_`` then it will
      be left alone. This option is not supported with ``as_needed``.
      Defaults to ``True``.

  Returns
  --------
  :class:`str`
      The text with the markdown special characters escaped with a slash.
  """

  if not as_needed:

    def replacement(match):
      groupdict = match.groupdict()
      is_url = groupdict.get('url')
      if is_url:
        return is_url
      return '\\' + groupdict['markdown']

    regex = _MARKDOWN_STOCK_REGEX
    if ignore_links:
      regex = f'(?:{_URL_REGEX}|{regex})'
    return re.sub(regex, replacement, text, count=0, flags=re.MULTILINE)
  else:
    text = re.sub(r'\\', r'\\\\', text)
    return _MARKDOWN_ESCAPE_REGEX.sub(r'\\\1', text)


def escape_mentions(text: str) -> str:
  """A helper function that escapes everyone, here, role, and user mentions.

  .. note::

      This does not include channel mentions.

  .. note::

      For more granular control over what mentions should be escaped
      within messages, refer to the :class:`~discord.AllowedMentions`
      class.

  Parameters
  -----------
  text: :class:`str`
      The text to escape mentions from.

  Returns
  --------
  :class:`str`
      The text with the mentions removed.
  """
  return re.sub(r'@(everyone|here|[!&]?[0-9]{17,20})', '@\u200b\\1', text)
