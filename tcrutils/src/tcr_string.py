import re as regex

from .tcr_int import clamp


def commafy(text: str | int, splitter: str = ','):
  """Commafy a number.

  Returns a string of that number split by commas if needed, or any character passed as splitter.
  """
  if isinstance(text, int) and text < 0:
    return '-' + commafy(-text)
  text = str(text)
  temp = ''
  for i, letter in enumerate(text[::-1]):
    temp += letter
    if i % 3 == 2 and i != len(text) - 1:
      temp += splitter
  return temp[::-1]


def join_urlstr(*urlstrs: str) -> str:
  """Join a sequence of urlstrs with '/'. Cleans up extra slashes."""
  s = [str(x).strip('/') for x in urlstrs]
  s = '/'.join(s)
  return regex.sub(r'/+', '/', s)


class SlashableString(str):
  """Represents a string that can be concatenated with another string along with a splitter by the use of the divide operator.

  Example:
  ```py
  s = SlashableString("a")
  s1 = s / 'c'
  print(repr(s1)) # -> 'a/c'
  ```
  Splitter can be changed with the `splitter` argument. (the splitter is '/' by default to be consistent with the division symbol)
  If strip argument is True, the string will be stripped of any leading or trailing splitters.
  If cleanup argument is True, the string will be cleaned up by replacing any double splitters with a single splitter (a.com//////b -> a.com/b).

  The floor division operator (`//`) is the same as the slash operator (`/`) except that it doesn't strip or cleanup the string afterwards, regardless of the settings.
  """

  def __new__(cls, o: object, **_) -> 'SlashableString':
    return super().__new__(cls, o)

  def __init__(self, o: object, *, splitter: str = '/', strip: bool = True, cleanup: bool = True) -> None:
    self.__splitter = str(splitter)
    self.__strip = strip
    self.__cleanup = cleanup

  def __truediv__(self, other: str) -> 'SlashableString':
    s = f'{self}{self.__splitter}{other}'

    if self.__cleanup:
      while f'{self.__splitter}{self.__splitter}' in s:
        s = s.replace(f'{self.__splitter}{self.__splitter}', self.__splitter)

    if self.__strip:
      s = s.strip(self.__splitter)

    return SlashableString(s, splitter=self.__splitter, strip=self.__strip, cleanup=self.__cleanup)

  def __floordiv__(self, other: str) -> 'SlashableString':
    return SlashableString(f'{self}{self.__splitter}{other}', splitter=self.__splitter, strip=self.__strip, cleanup=self.__cleanup)


def custom_zfill(value: int | str, fill_amount: int, fillchar: str = ' ') -> str:
  """
  Zfills the number to a certain length with a certain fill character.

  Supports negative numbers (- counts as a character when counting filling)

  Args:
    value (int): value to zfill
    fill_amount (int): how many chars in total must be in the zfilled string
    fillchar (str): character to use for filling

  Returns:
    str: zfilled string
  """
  v = str(abs(value)) if not isinstance(value, str) else value
  while len(v) < (fill_amount - (0 if isinstance(value, str) else (1 if value < 0 else 0))):
    v = fillchar + v
  return v if isinstance(value, str) else ('-' + v if value < 0 else v)


def polaris_progressbar(
  current: int,
  total: int = 100,
  *,
  width: int = 30,
  chars: str = '▓░',
  pattern: str = '%(bar)s %(current)s/%(total)s %(percent)s%%',
  percent_decimal_places: int = 2,
  zfill_to_total_width: bool = True,
  zfill_with: str = ' ',
) -> str:
  """Generate a progress bar for use in a terminal."""
  total = round(total)

  if width < 0:
    width = 0

  progress = int(width * clamp(0, current, total) / total)
  bar = chars[0] * progress + ' ' * (width - progress)

  percent = f'{100 * current / total:.{percent_decimal_places}f}'

  return pattern % {
    'bar': bar,
    'current': current if not zfill_to_total_width else custom_zfill(current, len(str(total)), zfill_with),
    'total': total,
    'percent': percent if not zfill_to_total_width else custom_zfill(percent, len(f'{100:.{percent_decimal_places}f}'), zfill_with),
  }
