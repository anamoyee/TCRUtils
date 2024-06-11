import collections.abc as _cabc
import typing as _t
from collections.abc import Awaitable as __Awaitable
from collections.abc import Callable as __Callable
from typing import Unpack as __Unpack

import hikari as _hk


class HikariDictMessage(_t.TypedDict):
  """Signature of some hikari respond() functions."""

  content: str
  attachment: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.files.Resourceish]]
  attachments: _t.NotRequired[_hk.undefined.UndefinedOr[_cabc.Sequence[_hk.files.Resourceish]]]
  component: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.api.CommandBuilder]]
  components: _t.NotRequired[_hk.undefined.UndefinedOr[_cabc.Sequence[_hk.api.ComponentBuilder]]]
  embed: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.Embed]]
  embeds: _t.NotRequired[_hk.undefined.UndefinedOr[_cabc.Sequence[_hk.Embed]]]
  sticker: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.snowflakes.SnowflakeishOr[_hk.PartialSticker]]]
  stickers: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.snowflakes.SnowflakeishSequence[_hk.PartialSticker]]]
  tts: _t.NotRequired[_hk.undefined.UndefinedOr[bool]]
  reply: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.snowflakes.SnowflakeishOr[_hk.PartialMessage]]]
  reply_must_exist: _t.NotRequired[_hk.undefined.UndefinedOr[bool]]
  mentions_everyone: _t.NotRequired[_hk.undefined.UndefinedOr[bool]]
  mentions_reply: _t.NotRequired[_hk.undefined.UndefinedOr[bool]]
  user_mentions: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.snowflakes.SnowflakeishSequence[_hk.users.PartialUser] | bool]]
  role_mentions: _t.NotRequired[_hk.undefined.UndefinedOr[_hk.snowflakes.SnowflakeishSequence[_hk.guilds.PartialRole] | bool]]
  flags: _t.NotRequired[_hk.undefined.UndefinedType | (int | _hk.MessageFlag)]


HikariResponder = __Callable[[__Unpack[HikariDictMessage]], __Awaitable[_hk.Message]]


hikari_dict_message_defaults = {
  'attachment': _hk.UNDEFINED,
  'attachments': _hk.UNDEFINED,
  'component': _hk.UNDEFINED,
  'components': _hk.UNDEFINED,
  'embed': _hk.UNDEFINED,
  'embeds': _hk.UNDEFINED,
  'sticker': _hk.UNDEFINED,
  'stickers': _hk.UNDEFINED,
  'tts': _hk.UNDEFINED,
  'reply': _hk.UNDEFINED,
  'reply_must_exist': _hk.UNDEFINED,
  'mentions_everyone': _hk.UNDEFINED,
  'mentions_reply': _hk.UNDEFINED,
  'user_mentions': _hk.UNDEFINED,
  'role_mentions': _hk.UNDEFINED,
  'flags': _hk.UNDEFINED,
}
