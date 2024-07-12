"""TCRUtils Discord. Contains various features related to bot development on discord and other stuff maybe."""


try:
  from . import tcrd_types as types
  from .tcrd_alias import get_guild_count
  from .tcrd_constants import DISCORD_EPOCH
  from .tcrd_dpy import escape_markdown, escape_mentions, remove_markdown
  from .tcrd_embeds import embed, modal
  from .tcrd_limits import DiscordLimits
  from .tcrd_permissions import PERMISSIONS_DICT, Permission, permissions
  from .tcrd_permissions import Permission as DiscordPermission
  from .tcrd_permissions import permissions as discord_permissions
  from .tcrd_shorts import confirm
  from .tcrd_snowflake import is_snowflake
  from .tcrd_string import IFYs, get_token
except ImportError: ...
