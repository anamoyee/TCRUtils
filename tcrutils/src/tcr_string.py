import re as regex


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
  print(repr(s)) # -> 'a/c'
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
