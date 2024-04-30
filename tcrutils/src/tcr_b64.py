import base64


class b64:
  def __init__(self) -> None:
    raise RuntimeError('This class should not be instantiated.')

  @staticmethod
  def encode(text: str, encoding: str = 'utf-8') -> str:
    return base64.b64encode(text.encode(encoding=encoding)).decode(encoding=encoding)

  @staticmethod
  def decode(text: str, encoding: str = 'utf-8') -> str:
    return base64.b64decode(text.encode(encoding=encoding)).decode(encoding=encoding)
