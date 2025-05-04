from collections.abc import Callable

from .extract_error import extract_error, extract_traceback
from .iterable import cut_at

BACKTICK = "`"
BACKTICKS = 3 * BACKTICK
NEWLINE = "\n"


def codeblock(
	text: str,
	*,
	langcode: str = "",
	max_length: int = 1984,
	cut_at_func: Callable[[str, int], str] = cut_at,
	smart_empty: bool = True,
) -> str:
	"""Pack text into a Discord codeblock.

	Note: May return str with len > max_length if max_length is ridicously low such that not even `'''\\nlangcode'''` fits

	Args:
	  text: The text to put in the codeblock body.
	  langcode: The language code to use in discord codeblock, for example "py".
	  max_length: The maximum length of the output str.
	  cut_at_func: A Callable[[str, int], str] which's returned string is of or less than the passed in int in length.
	  smart_empty: If true, if `text` is '' (an empty string) it will be changed to ' ' (a space). This prevents the codeblock to think langcode is the body of the codeblock if no text is supplied.
	"""
	if smart_empty and text == "":
		text = " "

	maxlen = (
		max_length - (len(BACKTICKS) + len(langcode) + len(NEWLINE) + len(BACKTICKS)) if max_length != -1 else 9999999999999999  # Eh...
	)
	return BACKTICKS + langcode + NEWLINE + cut_at_func(text, maxlen) + BACKTICKS


def uncodeblock(text: str) -> str:
	"""*Try to* remove any discord codeblocks along with their langcodes if any are found."""
	if text[-3:] == BACKTICKS and text[:3] == BACKTICKS:
		code_start = 3
		code_end = -3
		if NEWLINE in text[3:]:  # Check if there is a language code specified
			code_start = text.index(NEWLINE) + 1
		return text[code_start:code_end].strip()
	return text


def codeblocks(
	text1: str,
	*texts: str,
	langcodes: tuple[str] | None = None,
	max_length: int = 1984,
	cut_at_func: Callable[[str, int], str] = cut_at,
	smart_empty: bool = True,
):
	"""Mutliple-codeblock(). May suffer simillar issues as `codeblock`, like the total_max_length not actually being max because codeblock() may return something slightly longer.

	For more info read codeblock() docstring
	"""
	texts = text1, *texts

	if langcodes is None:
		langcodes = ("",) * len(texts)

	out = ""

	for text, langcode in zip(texts, langcodes, strict=True):
		out += codeblock(text, langcode=langcode, max_length=max_length - len(out), cut_at_func=cut_at_func, smart_empty=smart_empty)

	return out


def discord_exception(e: BaseException, *, max_length: int = 1800) -> str:
	return codeblocks(
		extract_error(e),
		extract_traceback(e),
		langcodes=(
			"txt",
			"py",
		),
		max_length=max_length,
		smart_empty=True,
	)
