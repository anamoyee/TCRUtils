"""Not to be confused with `tcrutils.lang`. This module is for natural language processing."""

from functools import wraps


def apostrophe_s(word: str):
	"""### Adds 's to a word unless it ends with s, then it adds only the apostrphe '.

	```py
	>>> apostrophe_s('Mark')
	"Mark's"
	>>> apostrophe_s('James')
	"James'"
	"""
	if word.endswith("s"):
		return word + "'"
	return word + "'s"


def plural_s(n: int, *, s: str = "s"):
	"""Return `'s'` if `n != 1` else `''`."""
	return s if n != 1 else ""


def _caps_deco(func):
	@wraps(func)
	def wrapper(word: str, *args, **kwargs):
		result = func(word, *args, **kwargs)
		if word.isupper():
			return result.upper()
		if word[0].isupper() and word[1:].islower():
			return result[0].upper() + result[1:].lower()
		return result

	return wrapper


irregular_plurals = {
	"child": "children",
	"man": "men",
	"woman": "women",
	"tooth": "teeth",
	"foot": "feet",
	"goose": "geese",
	"mouse": "mice",
	"ox": "oxen",
	"person": "people",
	"die": "dice",
	"criterion": "criteria",
	"phenomenon": "phenomena",
	"cactus": "cacti",
	"focus": "foci",
	"analysis": "analyses",
	"thesis": "theses",
	"crisis": "crises",
	"basis": "bases",
	"stimulus": "stimuli",
	"appendix": "appendices",
	"bacterium": "bacteria",
	"curriculum": "curricula",
	"index": "indices",
	"medium": "media",
	"millennium": "millennia",
	"radius": "radii",
	"memorandum": "memoranda",
	"vertex": "vertices",
	"belief": "beliefs",
	"chief": "chiefs",
	"roof": "roofs",
}


def make_plural(word: str, n: int = 2) -> str:
	"""### Tries its best to convert the word to plural if n != 1 else return the original word."""
	if n == 1:
		return word
	if word.lower() in irregular_plurals:
		return irregular_plurals[word.lower()]
	if word.lower().endswith(("s", "x", "z", "ch", "sh", "o")):
		return word + "es"
	if word.lower().endswith("y") and word[-2] not in "aeiou":
		return word[:-1] + "ies"
	if word.lower().endswith("f"):
		return word[:-1] + "ves"
	if word.lower().endswith("fe"):
		return word[:-2] + "ves"
	return word + "s"


globals()["make_plural"] = _caps_deco(make_plural)


def nth(n: int):
	"""### Return a string containing original number + numeric suffix (st, nd, rd, th).

	Takes into account edge cases like 11, 12.
	Supports negative numbers & zero.

	Examples:
	```py
	>>> nth(1)
	'1st'
	>>> nth(4)
	'4th'
	>>> nth(12)
	'12th'
	```
	"""
	if not isinstance(n, int):
		raise TypeError(n)

	if n < 0:
		return "-" + nth(-n)

	if 10 < n % 100 < 14:
		suffix = "th"
	else:
		match n % 10:
			case 1:
				suffix = "st"
			case 2:
				suffix = "nd"
			case 3:
				suffix = "rd"
			case _:
				suffix = "th"

	return str(n) + suffix
