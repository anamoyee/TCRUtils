def extract_error(value, pattern='%s: %s', *, raw=False):
  one = repr(value).split('(')[0]
  two = str(value)
  return (one, two) if raw else pattern % (one, two)
