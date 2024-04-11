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
