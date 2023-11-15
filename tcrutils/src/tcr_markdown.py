from .tcr_constants import BACKTICKS, NEWLINE, DiscordLimits


def codeblock(
  text: str,
  *,
  langcode='',
  max_length: int = DiscordLimits.Message.LENGTH_SAFE,
) -> str:
  """Pack text into a Discord codeblock.

  May return str with len > max_length if max_length is ridicously low such that not even ` ` `\\nlangcode` ` ` fit
  """
  maxlen = (
    max_length - (len(BACKTICKS) + len(langcode) + len(NEWLINE) + len(BACKTICKS))
    if max_length != -1
    else 9999999999999999 # Eh...
  )
  return BACKTICKS + langcode + NEWLINE + text[:maxlen] + BACKTICKS


def uncodeblock(text: str) -> str:
  """*Try to* remove any discord codeblocks along with their langcodes if any are found."""
  if text[-3:] == BACKTICKS and text[:3] == BACKTICKS:
    code_start = 3
    code_end = -3
    if NEWLINE in text[3:]:  # Check if there is a language code specified
      code_start = text.index(NEWLINE) + 1
    return text[code_start:code_end].strip()
  return text
