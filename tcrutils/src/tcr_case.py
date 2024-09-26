import re as _regex
from collections.abc import Iterable as _Iterable


def snake_to_camel(s: str, always_uppercase: _Iterable[str] = ("id",), unless_str_in_always_uppercase: bool = False) -> str:
	if unless_str_in_always_uppercase and s.lower() in always_uppercase:
		return s

	words = s.split("_")
	converted = words[0] + "".join(word.title() for word in words[1:])

	for word in always_uppercase:
		converted = converted.replace(word.title(), word.upper())

	return converted
