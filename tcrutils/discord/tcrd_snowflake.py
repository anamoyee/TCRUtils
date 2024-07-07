def is_snowflake(snowflake: int | str, *, allow_string=True) -> bool:
  if not isinstance(snowflake, ((int | str) if allow_string else int)):
    return False

  if not str(snowflake).isnumeric() or (int(snowflake) not in range(1 << 64)):
    return False

  return True
