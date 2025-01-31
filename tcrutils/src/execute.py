import re
from collections.abc import Callable, Iterable
from typing import Any, TypedDict

import attr as atr

from .console import console
from .run import run_sac


def _cut_string_at_indices(input_string, indices):
  return [input_string[i:j] for i, j in zip([0] + indices, indices + [None], strict=True)]


def _get_innermost_placeholders_indeces(text: str, R: str) -> list[int]:
  matches = re.finditer(R, text)
  spans = [match.span() for match in matches]
  return [item for t in spans for item in t]


def example_placeholder(name: str, *args: str, **kw) -> str:
  return name.upper()


def brackets_validator(inst, attr, value):
  if not isinstance(value, Iterable):
    raise TypeError('brackets must be an iterable')
  if not len(value) == 2:
    raise ValueError('brackets must be a tuple with two elements (opening and closing brackets)')
  if not all(isinstance(x, str) for x in value):
    raise TypeError('opening and closing brackets must be str')
  if len(value[0]) != len(value[1]):
    raise ValueError('opening and closing brackets must be the same length')


def placeholders_validator(inst, attr, value):
  if not isinstance(value, dict):
    raise TypeError('placeholders must be a dict')
  if not all(isinstance(x, str) for x in value):
    raise TypeError('placeholder keys must be str')
  if not all(callable(x) for x in value.values()):
    raise TypeError('placeholder keys must be str')


class MissingPlaceholderError(Exception): ...


@atr.s(kw_only=True)
class Execute:
  """r!execute from RoboTop."""

  brackets: tuple[str] = atr.ib(default=('{', '}'), validator=brackets_validator)
  splitter: str = atr.ib(default='|', validator=atr.validators.instance_of(str))
  placeholders: dict[str, Callable] = atr.ib(factory=dict, validator=placeholders_validator)

  def __attrs_post_init__(self) -> None:
    self.R = r'{[^{}]*}'.replace('{', re.escape(self.brackets[0])).replace('}', re.escape(self.brackets[1]))

  async def __call__(self, text, /, **kw):
    indices = _get_innermost_placeholders_indeces(text, self.R)

    if not indices:
      return text

    segments = _cut_string_at_indices(text, indices)

    segments = [((await self._execute_placeholder(x, **kw)) if (x.startswith(self.brackets[0]) and x.endswith(self.brackets[1])) else x) for x in segments]

    return await self(''.join(segments), **kw)

  async def _execute_placeholder(self, placeholder: str, **kw):
    splits = placeholder[len(self.brackets[0]) : -len(self.brackets[1])].split(self.splitter)
    name, *args = splits

    if name in self.placeholders:
      ret = await run_sac(self.placeholders[name], name, *args, **kw)
    else:
      ret = await self._default_placeholder(name, *args, **kw)

    return self._cleanse(ret)

  async def _default_placeholder(self, name, *ar, **kw):
    raise MissingPlaceholderError('Unknown placeholder: name')
    # return f'<unknown placeholder: {name!r}>'

  @staticmethod
  def _cleanse(text: Any) -> str:
    text = str(text)
    return text.replace('{', '[').replace('}', ']')

  def add_placeholder(self, name: str, func: Callable) -> None:
    placeholders_validator(None, None, {name: func})
    self.placeholders[name] = func
