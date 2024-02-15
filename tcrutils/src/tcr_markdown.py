from collections.abc import Callable

from ..discord.tcrd_limits import DiscordLimits
from .tcr_constants import BACKTICKS, NEWLINE
from .tcr_iterable import cut_at


def codeblock(
  text: str,
  *,
  langcode='',
  max_length: int = DiscordLimits.Message.LENGTH_SAFE,
  cut_at_func: Callable[[str, int], str] = cut_at,
) -> str:
  """Pack text into a Discord codeblock.

  May return str with len > max_length if max_length is ridicously low such that not even `'''\\nlangcode'''` fits
  """
  maxlen = (
    max_length - (len(BACKTICKS) + len(langcode) + len(NEWLINE) + len(BACKTICKS))
    if max_length != -1
    else 9999999999999999  # Eh...
  )
  return BACKTICKS + langcode + NEWLINE + cut_at_func(text, maxlen) + BACKTICKS


def uncodeblock(text: str) -> str:
  """*Try to* remove any discord codeblocks along with their langcodes if any are found."""
  if text[-3:] == BACKTICKS and text[:3] == BACKTICKS:
    code_start = 3
    code_end = -3
    if NEWLINE in text[3:]:  # Check if there is a language code specified
      code_start = text.index(NEWLINE) + 1
    return text[code_start:code_end].strip()
  return text
