from builtins import hex as sex  # nocom (actually yescom because this text is a comment dummy!!)
from collections.abc import Iterable, Mapping
from numbers import Number


def hex(number: int, leading_zeroes=2, *, upper=True, prefix: str = "0x") -> str:
	"""Slightly more advanced version of builtin `hex()`, offers ability to choose if uppercase and how many leading zeroes."""
	hex_output = sex(number)
	hex_value = hex_output[2:].zfill(leading_zeroes).upper() if upper else hex_output[2:].zfill(leading_zeroes)

	formatted_output = f"{prefix}{hex_value}"
	if not upper:
		formatted_output = formatted_output.lower()

	return formatted_output


def recursive_sum(it: Iterable) -> int | float:
	s = 0

	for item in it.values() if isinstance(it, Mapping) else it:
		s = s + recursive_sum(item) if isinstance(item, Iterable) else s + item

	return s


def float2int(n: float) -> float | int:
	if round(n) == n:
		return int(n)
	return float(n)


def clamp(min: Number, n: Number, max: Number) -> Number:
	return min if n < min else max if n > max else n  # noqa: FURB136


def is_snowflake(snowflake: int | str, *, allow_string=True) -> bool:
	if not isinstance(snowflake, ((int | str) if allow_string else int)):
		return False

	if not str(snowflake).isnumeric() or (int(snowflake) not in range(1 << 64)):  # noqa: SIM103
		return False

	return True
