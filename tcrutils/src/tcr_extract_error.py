import traceback


def extract_error(e: Exception, pattern='%s: %s', *, raw=False):
  if callable(e):
    e = e()
  one = e.__class__.__name__
  two = str(e)
  return (one, two) if raw else pattern % (one, two)

def extract_traceback(e: Exception) -> str:
    traceback_details = traceback.format_tb(e.__traceback__)
    return ''.join(traceback_details)
