from builtins import hex as sex  # nocom (actually yescom because this text is a comment dummy!!)


def hex(number: int, leading_zeroes=2, *, upper=True) -> str:
  """Slightly more advanced version of builtin `hex()`, offers ability to choose if uppercase and how many leading zeroes."""
  hex_output = sex(number)
  hex_value = (
    hex_output[2:].zfill(leading_zeroes).upper() if upper else hex_output[2:].zfill(leading_zeroes)
  )

  formatted_output = f'0x{hex_value}'
  if not upper:
    formatted_output = formatted_output.lower()

  return formatted_output
