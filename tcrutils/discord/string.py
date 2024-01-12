import os
import pathlib as p
import re as regex
from typing import Literal, NoReturn

from ..src.tcr_constants import BACKTICKS
from ..src.tcr_regex import RegexPreset

cleanse_replacement = {
  BACKTICKS: '\''*3,
  '`': '\'',
  '#': '%', # Couldn't find a good candidate
  '*': '^', # here neither, just use non-replacement
  '_': ''
}

def _cleanse_invalid_method(method: str) -> NoReturn:
  raise ValueError(f'Invalid method: {method} for codeblock_only')

def cleanse(
  s: str,
  *,
  codeblock_only: Literal['none', 'replace', 'remove', 'escape'] = 'none',
  heading: Literal['none', 'replace', 'remove', 'escape'] = 'remove',

):
  """### Cleanse string `s` of any discord markdown.

  Method: whether to 'none', 'replace', 'remove' or 'escape' markdown.
   - 'none' (or false-y) will skip that perticular type of markdown and not touch it.
   - 'replace' will take a simillar character and replace the markdown character with it, for example backtick -> apostrophe
   - 'remove' will remove any characters effectively replacing them with ''
   - 'escape' will prepend every instance of that character with a backslash ('\\\\\\\\')

  Parts examples:
   - Codeblock: `"\\`\\`\\`py\\\\nimport os; os.unlink(__file__)\\`\\`\\`"`
   - Heading: `"# H1 heading"`, `"## H2 heading"`

  If `codeblock_only != 'none'` disregard any other setting and modify/remove/whatever triple backticks only
  """

  if codeblock_only and codeblock_only != 'none':
    match codeblock_only:
      case 'replace':
        return s.replace(BACKTICKS, cleanse_replacement[BACKTICKS])
      case 'remove':
        return s.replace(BACKTICKS, '')
      case 'escape':
        return s.replace(BACKTICKS, '\\`\\`\\`')
      case method:
        _cleanse_invalid_method(method)
  else: # not codeblock_only
    match heading:
      case 'replace':
        s = s.replace('#', cleanse_replacement['#'])
      case 'remove':
        s = regex.sub(*RegexPreset.MARKDOWN_HEADING, s)
      case 'escape':
        s = regex.sub(*RegexPreset.MARKDOWN_HEADING_E, s)
      case method:
        _cleanse_invalid_method(method)

def get_token(filename: str = 'TOKEN.txt', depth=2) -> None | str:
  """Get the nearest file with name=filename (default 'TOKEN.txt') and return its stripped contents.

  This algoritm searches for files named TOKEN.txt (or custom name) in the current directory, then the parent directory, then the parent of parent and so on.
  The search continues up to depth `depth` (depth=0: current directory only, depth=1, current directory and its parent, etc.). If multiple files are found, return the closest one to the current directory.
  """
  def rexit(x):
    os.chdir(origin_path)
    return x

  origin_path = p.Path.cwd().absolute()

  print(origin_path)

  os.chdir(origin_path)

  f = (origin_path / filename)

  for i in range(depth+1):
    f = ((origin_path / '/'.join(['..'] * i)) / filename)
    if f.is_file():
      return rexit(f.read_text().strip())
