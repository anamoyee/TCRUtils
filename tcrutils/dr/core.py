from collections.abc import Callable, Mapping
from typing import Any

from ..discord.tcrd_types import HikariDictMessage
from ..src.tcr_console import breakpoint as bp
from ..src.tcr_dict import merge_dicts
from ..src.tcr_run import run_sac
from .error import *
from .util import _TT, _Token, build_placeholder_rich_return_value

### Lexer


class _DRLexer:
  text: str
  parens: tuple[str, str]
  pos: int
  tokens: list[_Token]

  def __init__(self, text: str, parens: tuple[str, str]) -> None:
    self.text = text
    self.parens = parens
    self.pos = -1  # Advancing first, then checking, so it's 1 less
    self.tokens = []

  def _advance(self, amount: int = 1) -> None:
    self.pos += amount

  def starts_with(self, s: str) -> bool:
    return self.text[self.pos : self.pos + len(s)] == s

  def fetch_text(self) -> str:
    if self.pos >= len(self.text):
      return ''
    s = ''
    while self.pos < len(self.text) and not self.starts_with(self.parens[0]) and not self.starts_with(self.parens[1]):
      s += self.text[self.pos]
      self._advance()

    self._advance(-1)
    return s

  def __call__(self) -> list[_Token]:
    while self.pos < len(self.text):
      self._advance()
      if self.starts_with(self.parens[0]):
        self.tokens.append(_Token(_TT.PAREN_OPEN))
        self._advance(len(self.parens[0]) - 1)
      elif self.starts_with(self.parens[1]):
        self.tokens.append(_Token(_TT.PAREN_CLOSE))
        self._advance(len(self.parens[1]) - 1)
      else:
        self.tokens.append(_Token(_TT.TEXT, self.fetch_text()))
    return self.tokens[:-1]


### Parser


class _DRParser:
  contexts: Mapping[str, Any]
  placeholders: dict[str | None, Callable[..., str]]
  tokens: list[_Token]
  error_on_missing_placeholder: bool

  def __init__(
    self,
    contexts: Mapping[str, Any],
    placeholders: dict[str, Callable[..., str]],
    splitter: str,
    tokens: tuple[_Token],
    error_on_missing_placeholder: bool,
    error_on_invalid_placeholder_return: bool,
    parens: tuple[str, str],
  ) -> None:
    self.contexts = {**contexts, '__splitter': splitter, '__parens': parens, '__vars': {}}
    self.placeholders = placeholders
    self.tokens = list(tokens)
    self.error_on_missing_placeholder = error_on_missing_placeholder
    self.error_on_invalid_placeholder_return = error_on_invalid_placeholder_return

  def __tcr_fmt__(self, fmt_iterable, **kwargs):
    return self.__repr__()

  def check_integrity(self) -> None:
    parens_counter = 0

    for arg in self.tokens:
      if arg.type == _TT.PAREN_OPEN:
        parens_counter += 1
      elif arg.type == _TT.PAREN_CLOSE:
        parens_counter -= 1

      if parens_counter < 0:
        raise DynamicResponseSyntaxError(f'Mismatched parenthesis (Closed an unopened section.)')
    if parens_counter != 0:
      raise DynamicResponseSyntaxError(f'Mismatched parenthesis (Open section left unclosed.)')

  async def process_single_placeholder(self, tokens: list[_Token]) -> list[_Token]:
    text: str = ''.join(x.value for x in tokens)

    args = text.split(self.contexts['__splitter'])

    if args[0] in self.contexts['__vars']:
      return [_Token(_TT.TEXT, self.contexts['__vars'][args[0]])]
    if self.error_on_missing_placeholder and args[0] not in self.placeholders:
      raise DynamicResponseMissingPlaceholderError(f'Placeholder {args[0]!r} not found.')
    if args[0] not in self.placeholders:
      return [_Token(_TT.TEXT, f'{self.contexts["__parens"][0]}{text}{self.contexts["__parens"][1]}')]
    ret = await run_sac(self.placeholders[args[0]], *args, **self.contexts)
    if ret is None:
      ret = ''

    if type(ret) is not str:  # noqa: E721
      if isinstance(ret, list | tuple):
        if all(isinstance(x, _Token) for x in ret):
          return list(ret)
        else:
          raise DynamicResponseSyntaxError(f'Placeholder {args[0]!r} returned a list but contains non-token elements.')
    else:
      return [_Token(_TT.TEXT, ret)]

    if self.error_on_invalid_placeholder_return:
      raise DynamicResponsePlaceholderInvalidReturnError(f'Placeholder {args[0]!r} did not return a string nor list of tokens. (ret={ret!r})')
    return [_Token(_TT.TEXT, str(ret))]

  async def process_placeholders(self, tokens: list[_Token]) -> list[_Token]:
    first_open_index = None
    first_close_index = None

    for token in tokens:
      if token.type == _TT.PAREN_OPEN:
        first_open_index = tokens.index(token)
      if token.type == _TT.PAREN_CLOSE:
        first_close_index = tokens.index(token)
        break

    if first_open_index is None and first_close_index is None:
      return tokens
    elif first_open_index is None or first_close_index is None:
      raise RuntimeError('Internal error how the fuck are parenthesis mismatched again')

    for token in tokens[first_open_index + 1 : first_close_index]:
      if token.type != _TT.TEXT:
        raise RuntimeError('Shit is broken again (internal error) report this fucking piece of shit not fucking working FUUUUCK!!!!!!!!')

    placeholder_text_tokens = tokens[first_open_index + 1 : first_close_index]

    try:
      # print(f"[DEBUG] Processing {'|'.join(x.value for x in placeholder_text_tokens)}")
      processed_text_tokens = await self.process_single_placeholder(placeholder_text_tokens)
    # except BaseException:
    #   ...
    except DynamicResponseError:
      raise
    except RecursionError as e:
      raise DynamicResponseRecursionError(f'{e}') from e
    except TypeError as e:
      if 'missing' in str(e) and 'required positional argument' in str(e):
        raise DynamicResponsePlaceholderTooFewArgumentsError(f'Placeholder {placeholder_text_tokens} requires more arguments than were provided.') from e
      raise DynamicResponsePythonErrorInPlaceholerError(f'An error occured within a placeholder {placeholder_text_tokens}.') from e
    except Exception as e:
      raise DynamicResponsePythonErrorInPlaceholerError(f'An error occured within a placeholder {placeholder_text_tokens}.') from e

    del tokens[first_open_index : first_close_index + 1]
    for tkn in processed_text_tokens[::-1]:
      tokens.insert(first_open_index, tkn)

    return await self.process_placeholders(tokens)

  async def __call__(self) -> tuple[str, dict]:
    self.check_integrity()

    processed = await self.process_placeholders(self.tokens[:])
    return ''.join(x.value for x in processed), self.contexts


### Dynamic Response Builder

RESP_CONTEXTS = (
  'content',
  'attachments',
  'components',
  'embed',
  'stickers',
  'tts',
  'reply',
  'reply_must_exist',
  'mentions_everyone',
  'mentions_reply',
  'user_mentions',
  'role_mentions',
  'flags',
)


class DynamicResponseResult(str):
  contexts: dict[str, Any]

  def __new__(cls, string, contexts):
    instance = super().__new__(cls, string)
    instance.contexts = contexts
    return instance

  @property
  def resp(self) -> HikariDictMessage:
    return merge_dicts({'content': self}, {x: y for x, y in self.contexts.items() if x in RESP_CONTEXTS})


class DynamicResponseBuilder:
  placeholders: dict[str, Callable]
  parens: tuple[str, str]
  splitter: str
  instance_contexts: dict[str, Any]

  def __init__(
    self,
    *placeholders: dict[str, Callable] | None,
    parens: tuple[str, str] = ('{', '}'),
    splitter: str = '|',
    error_on_missing_placeholder: bool = True,
    error_on_invalid_placeholder_return: bool = True,
    instance_contexts: dict[str, Any] | None = None,
    context_constructors: dict[str, Callable[[], Any]] = {},  # noqa: B006
  ) -> None:
    if not all(isinstance(x, dict) for x in placeholders):
      raise TypeError('placeholders must be a dict or list of dicts')
    placeholders = merge_dicts(*placeholders)

    self.placeholders = placeholders
    self.parens = parens
    self.splitter = splitter
    self.error_on_missing_placeholder = error_on_missing_placeholder
    self.error_on_invalid_placeholder_return = error_on_invalid_placeholder_return
    self.instance_contexts = instance_contexts or {}
    self.context_constructors = context_constructors

  async def __call__(self, text: str, **contexts: Any) -> DynamicResponseResult:
    tokens = _DRLexer(text, parens=self.parens)()
    parsed, contexts = await _DRParser(
      contexts={**self.instance_contexts, **{x: y() for x, y in self.context_constructors.items()}, **contexts},
      placeholders=self.placeholders,
      splitter=self.splitter,
      tokens=tokens,
      error_on_missing_placeholder=self.error_on_missing_placeholder,
      error_on_invalid_placeholder_return=self.error_on_invalid_placeholder_return,
      parens=self.parens,
    )()

    return DynamicResponseResult(parsed, contexts)  # noqa: RET504 , RUF100

  def add_placeholder(self, name: str, func: Callable) -> None:
    self.placeholders[name] = func
