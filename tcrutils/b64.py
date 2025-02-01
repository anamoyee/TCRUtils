import base64 as _base64


def encode(text: str, encoding: str = "utf-8") -> str:
	return _base64.b64encode(text.encode(encoding=encoding)).decode(encoding=encoding)


def decode(text: str, encoding: str = "utf-8") -> str:
	return _base64.b64decode(text.encode(encoding=encoding)).decode(encoding=encoding)
