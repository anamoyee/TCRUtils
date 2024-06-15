class Every:
  """Return True every N calls of this instance. Additionally you can look up the total number of calls using `.count` attribute.

  Example:
  ```py
  every = Every(10)
  for i in range(100):
    if every():
      print(i)
  ```
  """

  count: int
  every: int

  def __init__(self, every: int, *, start: int = 0):
    if every == 0:
      raise ZeroDivisionError('every cannot be zero due to imminent division')
    self.every = every
    self.count = start

  def __call__(self, every: int | None = None) -> bool:
    try:
      return self.count % (every if every is not None else self.every) == 0
    finally:
      self.count += 1
