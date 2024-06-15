"""TCRUtils Discord. Contains various features related to bot development on discord and other stuff maybe."""

from .tcrd_alias import get_guild_count
from .tcrd_constants import DISCORD_EPOCH
from .tcrd_dpy import escape_markdown, escape_mentions, remove_markdown
from .tcrd_limits import DiscordLimits
from .tcrd_snowflake import Snowflake, is_snowflake
from .tcrd_string import IFYs, get_token

try:
  from . import tcrd_types as types
  from .tcrd_embeds import embed, modal
  from .tcrd_permissions import PERMISSIONS_DICT, Permission, permissions
  from .tcrd_permissions import Permission as DiscordPermission
  from .tcrd_permissions import permissions as discord_permissions
  from .tcrd_shorts import confirm
except ImportError: ...

__all__ = ['DiscordLimits', 'DiscordPermission', 'discord_permissions', 'tcrd_embeds', 'is_snowflake', 'Snowflake', 'embed', 'modal', 'get_token', 'get_guild_count']
