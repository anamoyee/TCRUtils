def commafy(text: str | int, splitter: str = ','):
  if isinstance(text, int) and text < 0:
    return '-' + commafy(-text)
  text = str(text)
  temp = ''
  for i, letter in enumerate(text[::-1]):
    temp += letter
    if i % 3 == 2 and i != len(text) - 1:
      temp += splitter
  return temp[::-1]
