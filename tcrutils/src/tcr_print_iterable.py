def print_iterable(
  it: list | tuple | dict, *, recursive=True, raw=False
) -> str | None:  # Required for debugging (console object)
  if it == []:
    return '[]'
  if it == ():
    return '()'
  if it == {}:
    return '{}'
  if isinstance(it, dict):
    text = '{'
    for key, value in it.items():
      if recursive and isinstance(value, list | tuple | dict):
        value = print_iterable(value, raw=True).replace('\n', '\n  ')
      else:
        value = repr(value)
      text += f'\n  {key!r}: {value},'
    text += '\n}'
  else:
    text = '[' if isinstance(it, list) else '('
    for value in it:
      if recursive and isinstance(value, list | tuple | dict):
        value = print_iterable(value, raw=True).replace('\n', '\n  ')
      else:
        value = repr(value)
      text += f'\n  {value},'
    text += '\n]' if isinstance(it, list) else '\n)'

  if raw:
    return text
  print(text)
  return None
