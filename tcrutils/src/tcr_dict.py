from collections.abc import Generator, Hashable, Mapping
from typing import Any


def _check_strict(master: Mapping, slave: Mapping, *, recursive: bool) -> bool:
  for k, v in master.items():
    if k not in slave:
      return [k]
    if recursive and isinstance(v, Mapping) and isinstance(slave[k], Mapping):  # noqa: SIM102
      if (a := _check_strict(v, slave[k], recursive=recursive)) is not True:
        return [k, *a]
  return True


def dict_zip(dict1: Mapping, *dicts: Mapping) -> Generator[tuple[Hashable, Any], None, None]:
  """Zips dictionaries simillar to `zip()`, returns a generator which yields a tuple of (key, (value1, value2, value3)) for each key. This function does not support analogy of `zip()` non-strict mode, strict=True is implied (Each key must be in every single passed in dict)."""

  dicks = [dict1, *dicts]

  kys = dicks[0].keys()
  if any(kys != dick.keys() for dick in dicks):
    msg = 'Mismatched keys'
    raise ValueError(msg)

  for k, v in dicks[0].items():
    yield (k, (v, *(dick[k] for dick in dicks[1:])))


def merge_dicts(master: Mapping, slave: Mapping, *, recursive=True, strict=False) -> Mapping:
  """Merge dictionaries, made to prioritize the `master` dictionary and if key is not found there, then it takes from the `slave` dictionary.

  Optionally if `recursive=True`, then if the same key is a dict in both master and slave, merge dicts operation is performed on both of them.\\
  Optionally if `strict=True` it raises `ValueError` if there exists a key that is in master dictionary but not in slave dictionary.
  """
  merged = {}

  if strict and (a := _check_strict(master, slave, recursive=recursive)) is not True:
    msg = f'Strict check failed: there exists a key ({".".join(a)}) that is in master dictionary but not in slave dictionary'
    raise ValueError(msg)

  for key in master:
    if key in slave:
      if isinstance(master[key], dict) and isinstance(slave[key], dict) and recursive:
        merged[key] = merge_dicts(master[key], slave[key], recursive=True)
      else:
        merged[key] = master[key]
    else:
      merged[key] = master[key]

  for key in slave:
    if key not in merged:
      merged[key] = slave[key]

  return merged
